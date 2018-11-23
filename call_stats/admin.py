from django.contrib import admin

# Register your models here.

from call_stats.models import PhoneNumber, CallInfo, RepeatPeriod, WeekDay, Schedule


class PhoneNumbersAdmin(admin.ModelAdmin):
    pass


class CallInfoAdmin(admin.ModelAdmin):
    pass


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