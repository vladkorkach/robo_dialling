from django.contrib import admin
import csv
from django.http import HttpResponse

from call_stats.models import PhoneNumber, CallInfo, RepeatPeriod, WeekDay, Schedule, CeleryPhoneModel


class PhoneNumbersAdmin(admin.ModelAdmin):
    pass


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta

        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names + ["department", "organization"])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names] + [obj.phone_dialed.department, obj.phone_dialed.organization])

        return response

    export_as_csv.short_description = "Export Selected"


class CallInfoAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("phone_dialed", "time_before_hang", "date", "get_department", "get_organization")
    list_filter = ("phone_dialed", "time_before_hang", "date", "phone_dialed__organization", "phone_dialed__organization")
    actions = ["export_as_csv"]

    def get_department(self, obj):
        return obj.phone_dialed.department

    def get_organization(self, obj):
        return obj.phone_dialed.organization

    def get_queryset(self, request):
        return super(CallInfoAdmin, self).get_queryset(request).prefetch_related("phone_dialed")

    def phones(self, obj):
        return self.phone_dialed_set.all()


class RepeatPeriodAdmin(admin.ModelAdmin):
    pass


class WeekDayAdmin(admin.ModelAdmin):
    pass


class ScheduleAdmin(admin.ModelAdmin):
    pass


class CeleryPhoneModelAdmin(admin.ModelAdmin):
    fields = ("name", "organization", "department", "number", "title", "interval", "crontab", "enabled", "kwargs")


admin.site.register(PhoneNumber, PhoneNumbersAdmin)
admin.site.register(CallInfo, CallInfoAdmin)
admin.site.register(RepeatPeriod, RepeatPeriodAdmin)
admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(CeleryPhoneModel, CeleryPhoneModelAdmin)
