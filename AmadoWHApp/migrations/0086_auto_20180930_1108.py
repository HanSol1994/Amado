# Generated by Django 2.0.5 on 2018-09-30 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0085_auto_20180930_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='11:08:49', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='11:08:49', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='11:08:49', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]
