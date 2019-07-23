# Generated by Django 2.0.5 on 2018-09-11 11:50

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0047_auto_20180909_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='rem_vacations',
            field=models.FloatField(default=0, verbose_name='مانده مرخصی از قبل مرداد ماه'),
        ),
        migrations.AlterField(
            model_name='baseagreement',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-06-20', verbose_name='تاریخ توافق'),
        ),
        migrations.AlterField(
            model_name='employeepayment',
            name='payment_date',
            field=django_jalali.db.models.jDateField(default='1397-06-20', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='employeepayment',
            name='payment_do_date',
            field=django_jalali.db.models.jDateField(default='1397-06-20', verbose_name='تاریخ اعمال'),
        ),
        migrations.AlterField(
            model_name='lawconstant',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-06-20', unique=True, verbose_name='تاریخ قانون'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='extra_shift',
            field=models.FloatField(verbose_name='شیفت اضافه'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='off',
            field=models.FloatField(verbose_name='ایام تعطیل کاری'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='vacation_rem',
            field=models.FloatField(verbose_name='مرخصی نرفته'),
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-06-20', verbose_name='تاریخ'),
        ),
    ]
