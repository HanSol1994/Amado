# Generated by Django 2.1.2 on 2018-10-29 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0108_auto_20181029_1024'),
        ('AmadoFinance', '0050_remove_recedeimage_def_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='recedeimage',
            name='def_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='defacheck', to='AmadoWHApp.Branch', verbose_name='حساب معین'),
        ),
    ]