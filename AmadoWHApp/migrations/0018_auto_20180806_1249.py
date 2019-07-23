# Generated by Django 2.0.5 on 2018-08-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0017_auto_20180806_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestproduct',
            name='request_amount_sent',
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-05-15 ساعت 12:49', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='12:49:35', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='12:49:35', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='12:49:35', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]