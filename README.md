####setup
info will be provided later


####usage
log in to admin panel

set your twilio credentials here. Please note, calls don't work in test mode
```
http://yourdomain.com/admin/call_stats/twiliosetting/
```

In order to set up calls schedule use this page
```
http://yourdomain.com/admin/call_stats/celeryphonemodel/
```

Statistics will be shown on page
```
http://yourdomain.com/call_stats
```

####sync with twilio statistics

In order to change twilio synchronization settings, use this page

 
```
http://yourdomain.com/admin/django_celery_beat/periodictask/
```
task for synchronization 
```
SyncWithTwilioStats
```