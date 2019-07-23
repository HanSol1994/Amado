# Generated by Django 2.0.5 on 2018-09-03 16:03

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0038_auto_20180903_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birth_day',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
        migrations.AddField(
            model_name='person',
            name='nat_id',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='شماره ملی'),
        ),
    ]
