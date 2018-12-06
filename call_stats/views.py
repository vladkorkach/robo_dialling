from django.shortcuts import redirect
from django.template import loader
import re

from .models import CallStat, CeleryPhoneModel
from django.http import HttpResponse
from django.db.models import Count
import json
from datetime import timedelta, datetime
from django.utils import timezone
from .exporter import Exporter
from .call_maker import TwilioCaller, TwilioConnecter


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
            "minPeriod": "hh"
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

    week_count = CallStat.objects.filter(date__gte=monday_of_this_week).count()

    a = CallStat.objects.all()\
        .values('date', 'phone_dialed__organization')\
        .annotate(total=Count('phone_dialed'))\
        .order_by('date')\
        .prefetch_related("phone_dialed")\
        .filter(date__gte=timezone.now().date() - timedelta(days=2)).exclude(status__in=["sended", "wrong"])

    l = []
    names = []
    tmp = {}

    for data in a:
        names.append(data["phone_dialed__organization"])
        if "date" not in tmp:
            tmp["date"] = data["date"].strftime('%Y-%m-%d %H')
            tmp[data["phone_dialed__organization"]] = data['total']
        else:
            if tmp["date"] == data["date"].strftime('%Y-%m-%d %H'):
                if data["phone_dialed__organization"] in tmp:
                    tmp[data["phone_dialed__organization"]] += data['total']
                else:
                    tmp[data["phone_dialed__organization"]] = data['total']
            else:
                l.append(tmp)
                tmp = {}
                tmp["date"] = data["date"].strftime('%Y-%m-%d %H')
                tmp[data["phone_dialed__organization"]] = data['total']
        l.append(tmp)
    myset = set(names)
    names = list(myset)
    chart_object = generate_chart_object(names, l)

    connecter = TwilioConnecter()
    balance = connecter.get_balance()

    context = {
        "chart": json.dumps(chart_object),
        "twilio_balance": "{}".format(str(balance)),
        "total_this_week": week_count
    }
    return HttpResponse(template.render(context, request))


def upload_file(request):
    file_obj = request.FILES['db_file']
    try:
        Exporter(file_object=file_obj)
    except BaseException as e:
        print(e.args)

    return redirect("call_stats/celeryphonemodel")


def twilio_callback(request):
    sid = request.POST["CallSid"]
    to = request.POST["To"]
    status = request.POST["CallStatus"]

    connecter = TwilioConnecter()
    call_info = connecter.get_call_info(sid)

    call_stat = CallStat.objects.filter(sid=sid).first()
    call_stat.time_before_hang = call_info.duration
    call_stat.status = status

    call_stat.save()


def debug_call_route(request):
    if request.GET["action"] == "synchronize":
        connecter = TwilioConnecter()
        print(connecter.client.username)
        kw = {"start_time_after": "2015-01-01", "start_time_before": "2016-01-01"}
        # try:
        #     calls = connecter.get_calls_list(**kw)
        #     print(calls)
        # except Exception as e:
        #     print(e.args)
        # for c in calls:
        #     call_stat = CallStat.objects.filter(sid=c["sid"]).first()
        #     if call_stat:
        #         call_stat.time_before_hang = c["duration"]
        #         call_stat.status = c["status"]
        #         print(call_stat.__dict__)
        #         # call_stat.save()

    elif request.GET["action"] == "test_call":
        number = "15005550009"
        connecter = TwilioConnecter()
        caller = TwilioCaller(connecter.client)
        data = caller.make_call(number=number)

        # for number in numbers:
        #     print(number)
        #     info = CallStat(phone_dialed=number, time_before_hang=0, sid=sids[number.number], status="sended")
        #     infos.append(info)

        # CallStat.objects.bulk_create(infos)

        if data[0]:
            CallStat(phone_dialed=number, time_before_hang=0, sid=data[0].sid, status=data[0].status)
        else:
            debug_info = json.dumps(data[1])
            CallStat(phone_dialed=number, debug_info=debug_info, time_before_hang=0, sid=None, status="wrong")

    else:
        sid = request.GET["CallSid"]
        to = request.GET["To"]
        status = request.GET["CallStatus"]

        connecter = TwilioConnecter()
        call_info = connecter.get_call_info(sid)

        call_stat = CallStat.objects.filter(sid=sid).first()
        call_stat.time_before_hang = call_info.duration
        call_stat.status = status

        call_stat.save()
    return HttpResponse("debug only")
