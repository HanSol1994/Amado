# Generated by Django 2.0.5 on 2018-09-03 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0066_auto_20180903_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-06-12 ساعت 20:20', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='20:20:50', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='20:20:50', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='20:20:50', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]
