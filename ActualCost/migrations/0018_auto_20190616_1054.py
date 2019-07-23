# Generated by Django 2.1.2 on 2019-06-16 06:24

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('ActualCost', '0017_auto_20190508_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailactualcost',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال است'),
        ),
        migrations.AlterField(
            model_name='actualcost',
            name='date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='تاریخ ثبت قیمت'),
        ),
        migrations.AlterField(
            model_name='actualcost',
            name='from_date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='محاسبه از تاریخ'),
        ),
        migrations.AlterField(
            model_name='actualcost',
            name='to_date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='محاسبه تا تاریخ'),
        ),
        migrations.AlterField(
            model_name='cost',
            name='cost_date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='تاریخ ثبت قیمت'),
        ),
        migrations.AlterField(
            model_name='wastesale',
            name='payment_date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='تاریخ واریز'),
        ),
        migrations.AlterField(
            model_name='wastesale',
            name='sale_date',
            field=django_jalali.db.models.jDateField(default='1398-03-26', verbose_name='تاریخ فروش'),
        ),
    ]