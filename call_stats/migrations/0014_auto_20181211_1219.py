# Generated by Django 2.1.3 on 2018-12-11 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call_stats', '0013_auto_20181206_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='twiliosetting',
            name='test_account_sid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='twiliosetting',
            name='test_auth_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='twiliosetting',
            name='test_mode',
            field=models.BooleanField(default=True),
        ),
    ]
