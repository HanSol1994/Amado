# Generated by Django 2.0.5 on 2018-09-01 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0020_auto_20180901_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='add_user',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='confirm_user',
        ),
        migrations.AlterUniqueTogether(
            name='salarydetail',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='salarydetail',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='salarydetail',
            name='person',
        ),
        migrations.RemoveField(
            model_name='salarydetail',
            name='salary',
        ),
        migrations.DeleteModel(
            name='Salary',
        ),
        migrations.DeleteModel(
            name='SalaryDetail',
        ),
    ]