# Generated by Django 2.0.5 on 2018-08-13 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoFinance', '0006_auto_20180813_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_recipient',
        ),
    ]
