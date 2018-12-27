from django.shortcuts import redirect
from django.template import loader

from .models import CallStat
from django.http import HttpResponse
from django.db.models import F
import json
from datetime import timedelta
from django.utils import timezone
from .exporter import Exporter
from .call_maker import TwilioConnecter
from django.views.decorators.csrf import csrf_exempt


def generate_chart_object(names, data):
    """
    :param names: organization names for chart
    :param data: statistics to display
    :return: dict with amchart settings and data
    """
    graphs = []

    for n in names:
        tmp = {
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "bulletSize": 10,
            "lineThickness": 3,
            "bulletAlpha": 0,
            "valueField": n,
            "labelText": "[[key]]",
            "title": n,
            "bulletBorderThickness": 1,
            "fillColorsField": "lineColor",
            "legendValueText": "[[value]]",
            "lineColorField": "lineColor",
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
            "minPeriod": "mm"
        },
        "categoryField": "date",
        "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    }

    return chart_settings


def index(request):
    """
    view for building and preparing chart.
    :param request: usual django request
    :return:template with chart data
    """
    template = loader.get_template("call_stats/index.html")

    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    week_count = CallStat.objects.filter(date__gte=monday_of_this_week).count()
    week_success_count = CallStat.objects.filter(date__gte=monday_of_this_week).filter(status__in=["completed"]).count()
    week_wrong_count = CallStat.objects.filter(date__gte=monday_of_this_week).exclude(status__in=["completed", "queued"]).count()

    with_response = CallStat.objects.all()\
        .values('date', 'phone_dialed__organization', 'status', 'time_before_hang')\
        .annotate(total=F('time_before_hang'))\
        .order_by('date')\
        .prefetch_related("phone_dialed")\
        .filter(date__gte=timezone.now().date() - timedelta(days=2)).exclude(status__in=["queued", "ringing"])

    l = []
    names = []
    tmp = {}

    for data in with_response:
        names.append(data["phone_dialed__organization"])
        if "date" not in tmp:
            tmp["date"] = data["date"].strftime('%Y-%m-%d %H-%M-%S')
            tmp[data["phone_dialed__organization"]] = data['total']
            if data['status'] in ['wrong', 'canceled', 'no-answer']:
                tmp["lineColor"] = "#FF0000"
            else:
                tmp["lineColor"] = ""
        else:
            if tmp["date"] == data["date"].strftime('%Y-%m-%d %H-%M-%S'):
                if data["phone_dialed__organization"] in tmp:
                    tmp[data["phone_dialed__organization"]] += data['total']
                    if data['status'] in ['wrong', 'canceled', 'no-answer']:
                        tmp["lineColor"] = "#FF0000"
                    else:
                        tmp["lineColor"] = ""
                else:
                    tmp[data["phone_dialed__organization"]] = data['total']
                    if data['status'] in ['wrong', 'canceled', 'no-answer']:
                        tmp["lineColor"] = "#FF0000"
                    else:
                        tmp["lineColor"] = ""
            else:
                l.append(tmp)
                tmp = {}
                tmp["date"] = data["date"].strftime('%Y-%m-%d %H-%M-%S')
                tmp[data["phone_dialed__organization"]] = data['total']
                if data['status'] in ['wrong', 'canceled', 'no-answer']:
                    tmp["lineColor"] = "#FF0000"
                else:
                    tmp["lineColor"] = ""
        l.append(tmp)

    myset = set(names)
    names = list(myset)
    chart_object = generate_chart_object(names, l)

    connecter = TwilioConnecter()
    balance = connecter.get_balance()

    context = {
        "chart": json.dumps(chart_object),
        "twilio_balance": "{}".format(str(balance)),
        "total_this_week": week_count,
        "wrong": week_wrong_count,
        "success": week_success_count,
        "title": "chart"
    }
    return HttpResponse(template.render(context, request))


def upload_file(request):
    """
    route for export csv phone numbers data
    launches exporter script from exporter.py
    :param request:
    :return redirect back to admin CeleryPhoneModel page:
    """
    file_obj = request.FILES['db_file']
    try:
        Exporter(file_object=file_obj)
    except BaseException as e:
        print(e.args)

    return redirect("call_stats/celeryphonemodel")


@csrf_exempt
def twilio_callback(request):
    """
    route for twilio callback
    more information here:
    https://www.twilio.com/docs/voice/api/call?code-sample=code-create-a-call-and-specify-a-statuscallbackevent#statuscallback
    :param request:
    :return:
    """
    sid = request.POST["CallSid"]
    to = request.POST["To"]
    status = request.POST["CallStatus"]

    connecter = TwilioConnecter()
    call_info = connecter.get_call_info(sid)
    call_stat = CallStat.objects.filter(sid=sid).first()
    if call_info:
        call_stat.time_before_hang = call_info.duration
        call_stat.status = status
    else:
        call_stat.status = status

    call_stat.save()

    return HttpResponse('')
