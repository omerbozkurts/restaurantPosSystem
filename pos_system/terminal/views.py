from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    data = {
        "tables": range(10)
    }
    return render(request, "index.html",data)