# Generated by Django 2.0.5 on 2018-08-21 06:24

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0008_auto_20180813_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarydetail',
            name='days',
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='base',
            field=models.IntegerField(verbose_name='حقوق ثابت'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='fix',
            field=models.IntegerField(verbose_name='حقوق پایه'),
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=django_jalali.db.models.jDateField(default='1397-05-30', verbose_name='تاریخ'),
        ),
    ]
