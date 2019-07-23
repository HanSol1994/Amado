# Generated by Django 2.0.5 on 2018-09-30 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadoFinance', '0026_auto_20180930_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashpayment',
            name='cost_center',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='costccash', to='AmadoFinance.CostCenter', verbose_name='مرکز هزینه'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checkpayment',
            name='cost_center',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AmadoFinance.CostCenter', verbose_name='مرکز هزینه'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internetsale',
            name='test',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
