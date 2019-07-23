# Generated by Django 2.0.5 on 2018-08-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0009_auto_20180806_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_actual_price_1',
            field=models.IntegerField(blank=True, null=True, verbose_name='قیمت تمام شده نوع ۱'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_actual_price_2',
            field=models.IntegerField(blank=True, null=True, verbose_name='قیمت تمام شده نوع ۲'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='12:44:34', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='12:44:34', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='12:44:34', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]