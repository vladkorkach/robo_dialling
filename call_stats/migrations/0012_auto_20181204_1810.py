# Generated by Django 2.1.3 on 2018-12-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call_stats', '0011_twiliosetting_call_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twiliosetting',
            name='call_status',
        ),
        migrations.AddField(
            model_name='callstat',
            name='duration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='callstat',
            name='sid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='callstat',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
