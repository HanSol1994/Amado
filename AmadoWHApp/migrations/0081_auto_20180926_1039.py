# Generated by Django 2.0.5 on 2018-09-26 07:09

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0080_auto_20180919_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amadofood',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ موجودی'),
        ),
        migrations.AlterField(
            model_name='foodsale',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ فروش'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-07-04 ساعت 10:39', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-07-04', null=True, verbose_name='تاریخ درخواست'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='10:39:44', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-07-04', null=True, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='10:39:44', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-07-04', null=True, verbose_name='تاریخ ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='10:39:44', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='last_price_date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ آخرین قیمت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='rc_date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ دریافت'),
        ),
        migrations.AlterField(
            model_name='shoprequest',
            name='from_date',
            field=django_jalali.db.models.jDateField(default='1397-07-04', verbose_name='تاریخ خرید'),
        ),
    ]
