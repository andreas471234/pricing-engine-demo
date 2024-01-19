# utility function
def request_query_params_to_dict(query_params):
    data = dict()

    for key, val in dict(query_params).items():
        if isinstance(val, list) and len(val) == 1:
            data[key] = val[0]
        else:
            data[key] = val

    return data


def request_pagination(query_params):
    page = query_params.get("page", 1)
    page_size = query_params.get("page_size", 10)

    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        page = 1
        page_size = 10

    if page < 1:
        page = 1

    if page_size < 1:
        page_size = 10
    elif page_size > 500:
        page_size = 500

    return page, page_size

