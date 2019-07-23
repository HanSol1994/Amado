# Generated by Django 2.1.2 on 2019-02-05 14:53

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0114_auto_20181213_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitToUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ration', models.FloatField(default=1, verbose_name='تبدیل بزرگ به کوچک')),
                ('first_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funit', to='AmadoWHApp.Unit', verbose_name='واحد بزرگتر')),
            ],
            options={
                'verbose_name': 'تبدیل واحد',
                'verbose_name_plural': 'تبدیلات واحد ها',
            },
        ),
        migrations.AlterField(
            model_name='amadofood',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ موجودی'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='status',
            field=models.CharField(choices=[('registered', 'ثبت شده/در انتظار تایید'), ('confirmed', 'تایید شده'), ('byadmin', 'موجودی توسط مدیریت گرفته شده')], default='registered', max_length=16, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='branchwarehouse',
            name='submit_date',
            field=django_jalali.db.models.jDateTimeField(verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='foodsale',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ فروش'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-11-16 ساعت 18:23', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_change_date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ تغییر قیمت'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-11-16', null=True, verbose_name='تاریخ درخواست'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='18:23:14', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-11-16', null=True, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='18:23:14', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-11-16', null=True, verbose_name='تاریخ ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='18:23:14', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='last_price_date',
            field=django_jalali.db.models.jDateField(blank=True, default='1397-11-16', null=True, verbose_name='تاریخ آخرین قیمت'),
        ),
        migrations.AlterField(
            model_name='shopdetail',
            name='rc_date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ دریافت'),
        ),
        migrations.AlterField(
            model_name='shoprequest',
            name='from_date',
            field=django_jalali.db.models.jDateField(default='1397-11-16', verbose_name='تاریخ خرید'),
        ),
        migrations.AddField(
            model_name='unittounit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Product', verbose_name='محصول مربوطه'),
        ),
        migrations.AddField(
            model_name='unittounit',
            name='second_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sunit', to='AmadoWHApp.Unit', verbose_name='واحد کوچکتر'),
        ),
    ]