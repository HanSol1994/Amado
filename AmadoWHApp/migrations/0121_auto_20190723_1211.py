# Generated by Django 2.1.2 on 2019-07-23 07:41

from django.db import migrations, models
import django_jalali.db.models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0120_auto_20190618_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='branch_access',
            field=models.ManyToManyField(to='AmadoWHApp.Branch', verbose_name='دسترسی شعب'),
        ),
        migrations.AlterField(
            model_name='amadofood',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='confirm_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ تایید'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ موجودی'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='submit_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='foodsale',
            name='confirm_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ تایید'),
        ),
        migrations.AlterField(
            model_name='foodsale',
            name='date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ فروش'),
        ),
        migrations.AlterField(
            model_name='foodsale',
            name='submit_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1398-05-01 ساعت 12:10', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1398-05-01', null=True, verbose_name='تاریخ درخواست'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:57', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1398-05-01', null=True, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:57', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1398-05-01', null=True, verbose_name='تاریخ ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:57', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='last_price_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1398-05-01', null=True, verbose_name='تاریخ آخرین قیمت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='rc_date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ دریافت'),
        ),
        migrations.AlterField(
            model_name='shoprequest',
            name='confirm_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ تایید'),
        ),
        migrations.AlterField(
            model_name='shoprequest',
            name='from_date',
            field=django_jalali.db.models.jDateField(default='1398-05-01', verbose_name='تاریخ خرید'),
        ),
        migrations.AlterField(
            model_name='shoprequest',
            name='submit_date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='تاریخ ثبت'),
        ),
    ]
