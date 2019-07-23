# Generated by Django 2.0.5 on 2018-09-03 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AmadoAccounting', '0034_remove_salary_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='add_date',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='add_user',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='confirm_date',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='confirm_user',
        ),
        migrations.AddField(
            model_name='salarydetail',
            name='add_date',
            field=django_jalali.db.models.jDateTimeField(default='1397-03-28 20:38:00', verbose_name='تاریخ ثبت'),
        ),
        migrations.AddField(
            model_name='salarydetail',
            name='add_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_register_user', to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده'),
        ),
        migrations.AddField(
            model_name='salarydetail',
            name='confirm_date',
            field=django_jalali.db.models.jDateTimeField(default='1397-03-28 20:38:00', verbose_name='تاریخ تایید'),
        ),
        migrations.AddField(
            model_name='salarydetail',
            name='confirm_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_confirm_user', to=settings.AUTH_USER_MODEL, verbose_name='تایید کننده'),
        ),
    ]
