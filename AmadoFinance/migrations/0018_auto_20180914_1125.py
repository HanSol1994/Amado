# Generated by Django 2.0.5 on 2018-09-14 06:55

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoFinance', '0017_auto_20180911_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashpayment',
            name='payment_due_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_again_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ مراجعه مجدد به بانک'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ صدور'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_due_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ چک'),
        ),
        migrations.AlterField(
            model_name='fundpayment',
            name='payment_due_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_add_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_date',
            field=django_jalali.db.models.jDateField(default='1397-06-23', verbose_name='تاریخ فروش'),
        ),
    ]
