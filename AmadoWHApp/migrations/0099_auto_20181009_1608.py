# Generated by Django 2.0.5 on 2018-10-09 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0098_auto_20181009_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopdetail',
            name='definitive_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.DefinitiveProduct', verbose_name='کالای خاص'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.CharField(blank=True, default='1397-07-17 ساعت 16:08', max_length=32, null=True, verbose_name='تاریخ ارسال پیام'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_time',
            field=models.TimeField(blank=True, default='16:08:30', null=True, verbose_name='ساعت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestproduct',
            name='request_time',
            field=models.TimeField(blank=True, default='16:08:30', null=True, verbose_name='ساعت ثبت'),
        ),
        migrations.AlterField(
            model_name='requestproductvariance',
            name='request_time',
            field=models.TimeField(blank=True, default='16:08:30', null=True, verbose_name='ساعت ثبت مغایرت'),
        ),
    ]
