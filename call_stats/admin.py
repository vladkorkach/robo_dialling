from django.contrib import admin
import csv
from django.http import HttpResponse

from call_stats.models import PhoneNumber, CallInfo, RepeatPeriod, WeekDay, Schedule


class PhoneNumbersAdmin(admin.ModelAdmin):
    pass


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class CallInfoAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("phone_dialed", "time_before_hang", "date")
    list_filter = ("phone_dialed", "time_before_hang", "date")
    actions = ["export_as_csv"]


class RepeatPeriodAdmin(admin.ModelAdmin):
    pass


class WeekDayAdmin(admin.ModelAdmin):
    pass


class ScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(PhoneNumber, PhoneNumbersAdmin)
admin.site.register(CallInfo, CallInfoAdmin)
admin.site.register(RepeatPeriod, RepeatPeriodAdmin)
admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Schedule, ScheduleAdmin)