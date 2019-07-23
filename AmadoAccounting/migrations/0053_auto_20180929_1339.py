# Generated by Django 2.0.5 on 2018-09-29 10:09

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0052_role_is_direct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseagreement',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-07', verbose_name='تاریخ توافق'),
        ),
        migrations.AlterField(
            model_name='employeepayment',
            name='payment_date',
            field=django_jalali.db.models.jDateField(default='1397-07-07', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='employeepayment',
            name='payment_do_date',
            field=django_jalali.db.models.jDateField(default='1397-07-07', verbose_name='تاریخ اعمال'),
        ),
        migrations.AlterField(
            model_name='lawconstant',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-07', unique=True, verbose_name='تاریخ قانون'),
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-07', verbose_name='تاریخ'),
        ),
    ]
