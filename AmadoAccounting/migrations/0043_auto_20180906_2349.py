# Generated by Django 2.0.5 on 2018-09-06 19:19

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0042_baseagreement_snapp_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolehistory',
            name='finish_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ پایان'),
        ),
    ]
