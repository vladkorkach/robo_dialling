####setup
info will be provided later


####usage
log in to admin panel

set your twilio credentials here. Please note, calls don't work in test mode
```
http://yourdomain.com/admin/call_stats/twiliosetting/
```
fields

- test_mode - activate test mode (default True)
- account_sid - twilio account SID
- auth_token - twilio auth token
- test_twilio_sid - test twilio sid. Used only if test mode is True
- test_auth_token - test auth token. Used only if test mode is True
- user - default django user. Twilio works for admin account only for now

In order to set up calls schedule use this page
```
http://yourdomain.com/admin/call_stats/celeryphonemodel/
```

Statistics will be shown on page
```
http://yourdomain.com/call_stats
```

 - x-axis represents dates
 - y-axis represents time of call by organization (or sum of calls if several calls for one organization made in same time)
broken and not answered calls has red color

####sync with twilio statistics

In order to change twilio synchronization settings, use this page

 
```
http://yourdomain.com/admin/django_celery_beat/periodictask/
```
task for synchronization 
```
SyncWithTwilioStats
```

####front end chart view
call statuses

```
[
    "wrong", # twilio don't able to make call. See details in debug_info in CallStat model. custom status
    "completed", # twilio made call with success
    "queued", # call waits in queue
    "busy", # busy responce
    "no-answer", 
    "canceled", 
    "failed", 
    "initiated", 
    "ringing", 
    "in-progress"
]
```
More info
```
more details here
https://support.twilio.com/hc/en-us/articles/223132547-What-are-the-Possible-Call-Statuses-and-What-do-They-Mean-
```