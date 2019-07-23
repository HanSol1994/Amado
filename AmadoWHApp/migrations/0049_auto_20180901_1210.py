# Generated by Django 2.0.5 on 2018-09-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0048_auto_20180901_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-06-10 ساعت 12:10', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:15', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:15', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='12:10:15', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]