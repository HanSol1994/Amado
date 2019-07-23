# Generated by Django 2.0.5 on 2018-10-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0096_auto_20181008_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawproduct',
            name='report_index',
            field=models.IntegerField(default=-1, verbose_name='ردیف در گزارش'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-07-16 ساعت 14:15', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='14:15:29', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='14:15:29', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='14:15:29', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]
