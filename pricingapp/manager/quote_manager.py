import datetime
from decimal import Decimal
from itertools import groupby

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.serializers.quote_serializers import (
    CreatePOSerializer,
    QuoteDetailSerializer,
    QuoteListSerializer,
    QuotePriceSerializer,
)
from pricingapp.models import Quote
from pricingapp.models.fleet import Fleet
from pricingapp.models.product import Product
from pricingapp.models.quote import QuoteItem
from pricingapp.models.supplier import Supplier
from services.base_manager import BaseManager


class PricingEngine:
    def __init__(self, base_cost, profit_margin, market_price, avg_past_sell_price=0):
        self.base_cost = base_cost
        self.profit_margin = Decimal(profit_margin / 100)
        self.market_price = market_price
        self.avg_past_sell_price = avg_past_sell_price

    def calculate_price(self):
        # create dynamic margin 20% of current price difference
        dynamic_margin_percentage = Decimal(
            (self.market_price - self.avg_past_sell_price) / self.market_price,
        ) * Decimal(0.2)

        # calculate the margin
        final_margin_percentage = self.profit_margin + dynamic_margin_percentage
        profit_amount = self.base_cost * final_margin_percentage
        price = self.base_cost + profit_amount

        return price


class QuoteManager(BaseManager):
    def __init__(self, cust_obj=None, quote_obj=None):
        super().__init__()
        self.cust_obj = cust_obj
        self.quote_obj = quote_obj
        self.price_breakdown = None
        self.errors = None
        self.error_code = None

    @transaction.atomic
    def create_purchase_order(self, payload):
        serializer = CreatePOSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.data
            self.quote_obj = Quote.objects.create(
                customer=self.cust_obj,
                status=Quote.STATUS_COMPLETED,
                remarks="historical purchase order data",
                created_at=data["order_date"],
            )
            for item in data["orders"]:
                QuoteItem.objects.create(
                    quote=self.quote_obj,
                    product=Product.objects.get(code=item["product_code"]),
                    remarks="historical purchase order data",
                    order_quantity=item["qty"],
                    status=QuoteItem.STATUS_COMPLETED,
                    selling_price=item["selling_price"],
                )

            serializer = QuoteDetailSerializer(self.quote_obj)
            return HTTP_201_CREATED, serializer.data
        return HTTP_400_BAD_REQUEST, serializer.errors

    def get_product_price(self, item):
        product = Product.objects.get(code=item["product_code"])
        supp_prod_list = product.supplier_maps.filter(stock__gte=item["qty"])
        if not supp_prod_list.exists():
            return (
                0,
                False,
                f"Not enough stock for these product - {item['product_code']}",
            )

        # getting the average price from all the pricelist
        market_price_query_set = product.supplier_maps.aggregate(
            Avg("price_maps__price_per_unit")
        )
        prod_market_price = market_price_query_set["price_maps__price_per_unit__avg"]

        # get past selling data
        # can be filtered and give priority margin to most recent data
        past_sell_price = product.quote_items.aggregate(Avg("selling_price"))
        avg_past_sell_price = past_sell_price["selling_price__avg"]

        product_price = []
        total_weight = item["qty"] * product.weight

        min_price = None

        for supp_prod in supp_prod_list:
            supp_base_price = supp_prod.price_maps.first().price_per_unit

            pricing_engine = PricingEngine(
                supp_base_price, 20, prod_market_price, avg_past_sell_price
            )
            markup_price = pricing_engine.calculate_price()
            temp_shipping_price, _ = Fleet.calculate_price(
                total_weight, self.cust_obj.city, supp_prod.supplier.city
            )

            if not temp_shipping_price:
                return 0, False, f"Shipping is not covered - {item['product_code']}"

            shipping_price = Decimal(temp_shipping_price)

            total_prod_price = round(markup_price * Decimal(item["qty"]), 4)

            if min_price:
                # check if we can reduce cost from same supplier shipping
                sub_total = total_prod_price + shipping_price
                if min_price < sub_total:
                    continue

                min_price = sub_total
            else:
                min_price = total_prod_price + shipping_price

            product_price.append(
                {
                    "supplier": supp_prod.supplier,
                    "shipping": round(shipping_price, 4),
                    "prices_per_unit": round(markup_price, 4),
                    "total_prod_price": total_prod_price,
                    "temp_with_shipping": round((total_prod_price + shipping_price), 4),
                }
            )

        data = {
            "product": product.code,
            "qty": item["qty"],
            "weight": total_weight,
            "prices": product_price,
        }

        return data, True, ""

    @staticmethod
    def group_supplier(k):
        return k["supplier_code"]

    def get_shipping_price(self, prod_price_matched):
        shipping_detail = []
        total_shipping = 0
        sorted_prod_prices = sorted(
            prod_price_matched, key=lambda d: d["supplier_code"]
        )
        for supplier_code, value in groupby(sorted_prod_prices, self.group_supplier):
            value_list = list(value)
            supp_weight = 0
            product_list = []
            for item in value_list:
                supp_weight += item["weight"]
                product_list.append(item["product_code"])

            shipping_price, _ = Fleet.calculate_price(
                supp_weight, self.cust_obj.city, value_list[0]["supplier_city"]
            )

            total_shipping += shipping_price

            shipping_detail.append(
                {
                    "supplier_code": supplier_code,
                    "product_list": product_list,
                    "total_weight": supp_weight,
                    "shipping_price": round(shipping_price, 4),
                }
            )

        return total_shipping, shipping_detail

    def get_best_price(
        self,
        chosen_supplier_code,
        total_price,
        prod_price_matched,
        prod_price_ambiguous,
        supp_checked=False,
    ):
        for prod in prod_price_ambiguous:
            prices = prod["prices"]
            if not supp_checked:
                for supp_price in prices:
                    if supp_price["supplier"].code in chosen_supplier_code:
                        prod_price_ambiguous.remove(prod)
                        prod["prices"] = [supp_price]
                        prod_price_matched.append(self.prepare_matched_prod_data(prod))
                        total_price += supp_price["total_prod_price"]
            else:
                min_total_price = 0
                best_price = None
                for price in prices:
                    if min_total_price == 0:
                        min_total_price = price["temp_with_shipping"]
                        best_price = price
                    if price["temp_with_shipping"] < min_total_price:
                        best_price = price
                total_price += best_price["total_prod_price"]
                prod_price_ambiguous.remove(prod)
                prod["prices"] = [best_price]
                prod_price_matched.append(self.prepare_matched_prod_data(prod))
                chosen_supplier_code.append(best_price["supplier"].code)

                if len(prod_price_ambiguous) >= 1:
                    prod_price_matched, total_price = self.get_best_price(
                        chosen_supplier_code,
                        total_price,
                        prod_price_matched,
                        prod_price_ambiguous,
                    )

                return prod_price_matched, total_price

        if len(prod_price_ambiguous) >= 1:
            prod_price_matched, total_price = self.get_best_price(
                chosen_supplier_code,
                total_price,
                prod_price_matched,
                prod_price_ambiguous,
                True,
            )

        return prod_price_matched, total_price

    def prepare_matched_prod_data(self, supp_prod_data):
        data = {
            "product_code": supp_prod_data["product"],
            "supplier_code": supp_prod_data["prices"][0]["supplier"].code,
            "supplier_city": supp_prod_data["prices"][0]["supplier"].city,
            "weight": supp_prod_data["weight"],
            "qty": supp_prod_data["qty"],
            "price": round(supp_prod_data["prices"][0]["total_prod_price"], 4),
        }
        return data

    def get_price(self, payload):
        # item = payload['orders'][0]
        prod_price_matched = []
        prod_price_ambiguous = []
        total_price = 0
        prod_prices = []
        chosen_supplier_code = []
        for item in payload["orders"]:
            prod_price_data, status, message = self.get_product_price(item)
            if not status:
                return HTTP_400_BAD_REQUEST, message

            prod_prices = prod_price_data["prices"]
            if len(prod_prices) == 1:
                matched_price_data = self.prepare_matched_prod_data(prod_price_data)
                prod_price_matched.append(matched_price_data)
                total_price = total_price + matched_price_data["price"]
                if matched_price_data["supplier_code"] not in chosen_supplier_code:
                    chosen_supplier_code.append(matched_price_data["supplier_code"])
            else:
                prod_price_ambiguous.append(prod_price_data)

        prod_price_matched, total_price = self.get_best_price(
            chosen_supplier_code, total_price, prod_price_matched, prod_price_ambiguous
        )

        total_shipping, shipping_detail = self.get_shipping_price(prod_price_matched)

        response = {
            "subtotal_price": round(total_price, 4),
            "shipping_price": round(total_shipping, 4),
            "total_payable": round((total_price + total_shipping), 4),
            "orders": prod_price_matched,
            "shipping_details": shipping_detail,
        }

        serializer = QuotePriceSerializer(data=response)
        if not serializer.is_valid():
            return HTTP_400_BAD_REQUEST, serializer.errors
        self.price_breakdown = serializer.data

        return HTTP_200_OK, self.price_breakdown

    @transaction.atomic
    def create_quote(self):
        created_date = datetime.datetime.now()
        expiry_time = created_date + datetime.timedelta(hours=1)
        self.quote_obj = Quote.objects.create(
            customer=self.cust_obj,
            expiry_date=expiry_time,
            price_breakdown=self.price_breakdown,
            payable_amount=self.price_breakdown["total_payable"],
        )
        for item in self.price_breakdown["orders"]:
            QuoteItem.objects.create(
                quote=self.quote_obj,
                product=Product.objects.get(code=item["product_code"]),
                supplier=Supplier.objects.get(code=item["supplier_code"]),
                order_quantity=item["qty"],
            )

        serializer = QuoteDetailSerializer(self.quote_obj)
        return HTTP_201_CREATED, serializer.data

    def get_detail(self):
        serializer = QuoteDetailSerializer(self.quote_obj)

        return HTTP_200_OK, serializer.data

    @staticmethod
    def _get_quote_queryset(query_params):
        filters = {
            "quote_no": query_params.get("quote_no", ""),
            "code": query_params.get("code", ""),
            "name": query_params.get("name", ""),
            "status": query_params.get("status", "").split(","),
        }

        verification_queryset = Quote.get_list(filters)

        return verification_queryset

    @classmethod
    def get_quote_list(cls, query_params, page=None, page_size=10):
        quote_queryset = cls._get_quote_queryset(query_params)

        if page and page_size:
            paginator = Paginator(quote_queryset, page_size)
            total_count = paginator.count
            num_pages = paginator.num_pages
            quote_queryset = paginator.get_page(page)
        else:
            total_count = len(quote_queryset)
            num_pages = 1
            page = 1

        data = QuoteListSerializer(quote_queryset, many=True).data
        resp = {
            "data": data,
            "meta_data": {
                "total_records": total_count,
                "page_size": page_size,
                "num_page": num_pages,
                "page": min(page, num_pages),
            },
        }

        return resp
