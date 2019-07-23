# Generated by Django 2.1.2 on 2018-10-29 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoWHApp', '0107_auto_20181029_1018'),
        ('AmadoFinance', '0047_remove_recedeimage_def_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='recedeimage',
            name='def_account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='defacheck', to='AmadoWHApp.Branch', verbose_name='حساب معین'),
            preserve_default=False,
        ),
    ]
