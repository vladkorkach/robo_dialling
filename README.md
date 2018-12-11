####usage
log in to admin panel

set your twilio credentials here
```
http://yourdomain.com/admin/call_stats/twiliosetting/
```

go to phone settings by following url
```
http://yourdomain.com/admin/call_stats/celeryphonemodel/
```

set up phone numbers and intervals for calls

Statistics will be shown on page
```
http://yourdomain.com/call_stats
```

####sync with twilio statistics

go to admin panel 

create new task 
```
http://yourdomain.com/admin/django_celery_beat/periodictask/
```
task for synchronization 
```
SyncWithTwilioStats
```