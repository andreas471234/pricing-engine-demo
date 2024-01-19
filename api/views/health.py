from django.http import HttpResponse


def view(_):
    return HttpResponse("OK")
