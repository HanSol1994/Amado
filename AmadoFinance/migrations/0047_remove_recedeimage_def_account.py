# Generated by Django 2.1.2 on 2018-10-29 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoFinance', '0046_recedeimage_def_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recedeimage',
            name='def_account',
        ),
    ]
