from django.shortcuts import render
from django.template import loader
from .models import CallStat
from django.http import HttpResponse


def index(request):
    template = loader.get_template("call_stats/index.html")
    context = {
        "stats": {}
    }
    return HttpResponse(template.render(context, request))
