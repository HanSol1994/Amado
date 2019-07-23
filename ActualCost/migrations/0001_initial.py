# Generated by Django 2.0.5 on 2018-09-30 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AmadoAccounting', '0054_auto_20180930_2006'),
        ('AmadoWHApp', '0091_auto_20180930_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='ACProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=128, verbose_name='نام محصول')),
                ('product_unit_rate', models.FloatField(default=0, verbose_name='واحد اول دارای این مقدار از واحد دوم است')),
                ('product_price_unit', models.BooleanField(default=True, verbose_name='واحد قیمت واحد دوم است')),
                ('product_process', models.CharField(choices=[('dried', 'خشک'), ('wet_p', 'تر فرآوری شده'), ('wet_np', 'تر فرآوری نشده')], default='dried', max_length=16, verbose_name='فرآوری محصول')),
                ('product_price_parameter', models.IntegerField(default=1, verbose_name='چندمین بزرگترین قیمت')),
                ('product_description', models.TextField(blank=True, max_length=256, null=True, verbose_name='توضیحات محصول')),
                ('product_weekly_consumption', models.FloatField(default=0, verbose_name='مصرف هفتگی')),
                ('product_is_active', models.BooleanField(default=False, verbose_name='کالا فعال می باشد')),
                ('product_level', models.CharField(choices=[('lvl1', 'ماده خام'), ('lvl2', 'مواد اولیه فرآوری شده'), ('lvl3', 'غذای آمادو')], default='lvl1', max_length=32, verbose_name='سطح محصول')),
                ('product_monthly_storage', models.FloatField(default=0, verbose_name='ماندگاری محصول(بر اساس ماه)')),
                ('definitive_food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.AmadoFood', verbose_name='غذای معین')),
                ('definitive_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Product', verbose_name='کالای معین')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات و قیمت تمام شده',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name', models.CharField(max_length=64, unique=True, verbose_name='نام پارامتر')),
                ('parameter_description', models.CharField(blank=True, max_length=128, null=True, verbose_name='توضیح پارامتر')),
                ('parameter_is_active', models.BooleanField(default=True, verbose_name='پارامتر فعال است')),
            ],
            options={
                'verbose_name': 'پارامتر',
                'verbose_name_plural': 'پارامتر ها',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_amount', models.FloatField(verbose_name='میزان ماده تشکیل دهنده در ۱ واحد از محصول')),
                ('recipe_child_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='ActualCost.ACProduct', verbose_name='محصول نهایی')),
                ('recipe_parent_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='ActualCost.ACProduct', verbose_name='ماده تشکیل دهنده')),
                ('recipe_unit', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Unit', verbose_name='واحد مقدار')),
            ],
            options={
                'verbose_name': 'دستور تهیه',
                'verbose_name_plural': 'دستور های تهیه',
            },
        ),
        migrations.AddField(
            model_name='acproduct',
            name='parameters',
            field=models.ManyToManyField(to='ActualCost.Parameter', verbose_name='پارامتر های قیمت تمام شده'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='prodcut_divisions',
            field=models.ManyToManyField(blank=True, null=True, to='AmadoAccounting.Division', verbose_name='بخش های مربوطه'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='product_actual_cost',
            field=models.ManyToManyField(blank=True, null=True, related_name='actual_cost', to='AmadoWHApp.Price', verbose_name='قیمت تمام شده ها'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='product_recipe',
            field=models.ManyToManyField(through='ActualCost.Recipe', to='ActualCost.ACProduct', verbose_name='مواد تشکیل دهنده ۱ واحد از محصول'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='product_sale_prices',
            field=models.ManyToManyField(blank=True, null=True, related_name='sale_price', to='AmadoWHApp.Price', verbose_name='قیمت فروش'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='product_second_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='second', to='AmadoWHApp.Unit', verbose_name='واحد دوم: قیمت محصول'),
        ),
        migrations.AddField(
            model_name='acproduct',
            name='product_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadoWHApp.Unit', verbose_name='واحد اول: خرید محصول'),
        ),
    ]