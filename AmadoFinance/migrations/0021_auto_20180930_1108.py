# Generated by Django 2.0.5 on 2018-09-30 07:38

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0086_auto_20180930_1108'),
        ('AmadoFinance', '0020_auto_20180926_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='عنوان')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AmadoWHApp.Branch', verbose_name='شعبه')),
            ],
            options={
                'verbose_name': 'مرکز هزینه',
                'verbose_name_plural': 'مراکز هزینه',
            },
        ),
        migrations.AlterField(
            model_name='cashpayment',
            name='payment_due_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_again_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ مراجعه مجدد به بانک'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ صدور'),
        ),
        migrations.AlterField(
            model_name='checkpayment',
            name='check_due_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ چک'),
        ),
        migrations.AlterField(
            model_name='fundpayment',
            name='payment_due_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ پرداخت'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_add_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_date',
            field=django_jalali.db.models.jDateField(default='1397-07-08', verbose_name='تاریخ فروش'),
        ),
    ]