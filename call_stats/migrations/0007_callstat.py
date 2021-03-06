# Generated by Django 2.1.3 on 2018-11-27 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('call_stats', '0006_auto_20181127_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_before_hang', models.IntegerField()),
                ('phone_is_active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('phone_dialed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='call_stats.CeleryPhoneModel')),
            ],
        ),
    ]
