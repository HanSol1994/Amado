# Generated by Django 2.1.2 on 2018-10-29 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0110_auto_20181029_1030'),
        ('AmadoFinance', '0052_auto_20181029_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='recedeimage',
            name='def_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='defacheck', to='AmadoWHApp.Branch', verbose_name='حساب معین'),
        ),
    ]