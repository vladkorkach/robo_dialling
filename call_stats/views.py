from django.shortcuts import render
from django.template import loader
from .models import CallStat
from django.http import HttpResponse
from django.db.models import Count, Sum
import json
from operator import itemgetter


def generate_chart_object(names, data):
    chart_settings = {
        "type": "serial",
        "theme": "light",
        "dataProvider": data,
        "graphs": [
            {
                "bullet": "round",
                "valueField": "Yahoo",
                "labelText": "[[key]]",
                "title": "yahoo"
            },
            {
                "bullet": "round",
                "valueField": "Google",
                "labelText": "[[key]]",
                "title": "google"
            }
        ],
        "legend": {
            "useGraphSettings": True,
        },
        "categoryAxis": {
            "parseDates": True,
            "minPeriod": "ss"
        },
        "categoryField": "date",
        "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    }

    return chart_settings


def index(request):
    template = loader.get_template("call_stats/index.html")
    a = CallStat.objects.all().values('phone_dialed__callstat__date', 'phone_dialed__organization').annotate(total=Count('phone_dialed')).prefetch_related("phone_dialed")
    l = []
    tmp = {}
    for data in a:

        if "date" not in tmp:
            tmp["date"] = data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S')
            print(tmp["date"])
            tmp[data["phone_dialed__organization"]] = data['total']
        else:
            print("2", tmp["date"])
            if tmp["date"] == data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S'):
                if data["phone_dialed__organization"] in tmp:
                    print(tmp)
                    tmp[data["phone_dialed__organization"]] += data['total']
                else:
                    tmp[data["phone_dialed__organization"]] = data['total']
            else:
                l.append(tmp)
                tmp = {}
                tmp["date"] = data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S')
                tmp[data["phone_dialed__organization"]] = data['total']
        # tmp = {
        #     "date": data["phone_dialed__callstat__date"].strftime('%H-%M-%S'),
        #     data["phone_dialed__organization"]: data['total']
        # }
        # l.append(tmp)
    print(l)
    chart_object = generate_chart_object(["Yahoo", "Google"], l)
    context = {
        "chart": json.dumps(chart_object)
    }
    return HttpResponse(template.render(context, request))
