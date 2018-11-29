from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from .models import CallStat
from django.http import HttpResponse
from django.db.models import Count, Sum
import json
from datetime import timedelta
from django.utils import timezone
from .importer import Importer


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

    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    week_count = CallStat.objects.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week).count()

    # print(week_count)

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

    myset = set(names)
    names = list(myset)
    chart_object = generate_chart_object(names, l)
    context = {
        "chart": json.dumps(chart_object),
        "twilio_balance": 0,
        "total_this_week": week_count
    }
    return HttpResponse(template.render(context, request))


def upload_file(request):
    name = request.POST.get("db_name")
    file_obj = request.FILES['db_file']
    Importer(file_object=file_obj)

    return redirect(reverse("admin:api_{}_changelist".format(name)))
