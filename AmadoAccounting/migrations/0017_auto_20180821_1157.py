# Generated by Django 2.0.5 on 2018-08-21 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoAccounting', '0016_auto_20180821_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarydetail',
            name='tax_min',
        ),
        migrations.AddField(
            model_name='salary',
            name='tax_min',
            field=models.IntegerField(default=0, verbose_name='حداقل پایه حقوق برای محاسبه مالیات'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='bime_fee',
            field=models.IntegerField(verbose_name='بیمه'),
        ),
    ]