# Generated by Django 2.1.2 on 2018-10-29 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoFinance', '0049_auto_20181029_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recedeimage',
            name='def_account',
        ),
    ]