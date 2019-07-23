# Generated by Django 2.0.5 on 2018-10-03 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AmadoFinance', '0031_auto_20181003_1044'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AmadoWHApp', '0092_auto_20181003_1044'),
        ('ActualCost', '0002_auto_20181003_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='WasteProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'کالای ضایعات',
                'verbose_name_plural': 'کالاهای ضایعات',
            },
        ),
        migrations.CreateModel(
            name='WasteSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', django_jalali.db.models.jDateField(default='1397-07-11', verbose_name='تاریخ فروش')),
                ('payment_date', django_jalali.db.models.jDateField(default='1397-07-11', verbose_name='تاریخ واریز')),
                ('status', models.CharField(choices=[('registered', 'ثبت شده'), ('confirmed', 'تایید شده'), ('rejected', 'رد شده'), ('paid', 'پرداخت شده')], default='registered', max_length=16, verbose_name='وضعیت')),
                ('submit_date', django_jalali.db.models.jDateTimeField(default='1397-03-28 20:38:00', verbose_name='تاریخ ثبت')),
                ('confirm_date', django_jalali.db.models.jDateTimeField(default='1397-03-28 20:38:00', verbose_name='تاریخ تایید')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoFinance.BankAccount', verbose_name='حساب واریزی')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Supplier', verbose_name='خریدار')),
                ('confirm_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wcu', to=settings.AUTH_USER_MODEL, verbose_name='تایید کننده')),
                ('submit_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wau', to=settings.AUTH_USER_MODEL, verbose_name='کاربر ثبت کننده')),
            ],
            options={
                'verbose_name': 'کالای ضایعات',
                'verbose_name_plural': 'کالاهای ضایعات',
            },
        ),
        migrations.CreateModel(
            name='WasteSaleProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='مقدار')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoFinance.CostCenter', verbose_name='مبدا')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ActualCost.WasteProduct', verbose_name='کالا')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Unit', verbose_name='واحد')),
            ],
            options={
                'verbose_name': 'جزئیات ضایعات',
                'verbose_name_plural': 'جزئیات ضایعات ها',
            },
        ),
    ]
