from django.template import loader
from .models import CallStat
from django.http import HttpResponse
from django.db.models import Count, Sum
import json


def generate_chart_object(names, data):
    graphs = []

    for n in names:
        tmp = {
            "bullet": "round",
            "valueField": n,
            "labelText": "[[key]]",
            "title": n
        }

        graphs.append(tmp)

    chart_settings = {
        "type": "serial",
        "theme": "light",
        "dataProvider": data,
        "graphs": graphs,
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
    names = []
    tmp = {}
    for data in a:
        names.append(data["phone_dialed__organization"])
        if "date" not in tmp:
            tmp["date"] = data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S')
            tmp[data["phone_dialed__organization"]] = data['total']
        else:
            if tmp["date"] == data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S'):
                if data["phone_dialed__organization"] in tmp:
                    tmp[data["phone_dialed__organization"]] += data['total']
                else:
                    tmp[data["phone_dialed__organization"]] = data['total']
            else:
                l.append(tmp)
                tmp = {}
                tmp["date"] = data["phone_dialed__callstat__date"].strftime('%Y-%m-%d %H-%M-%S')
                tmp[data["phone_dialed__organization"]] = data['total']
    # print(l)
    myset = set(names)
    names = list(myset)
    chart_object = generate_chart_object(names, l)
    context = {
        "chart": json.dumps(chart_object)
    }
    return HttpResponse(template.render(context, request))
