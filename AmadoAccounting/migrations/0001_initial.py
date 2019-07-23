# Generated by Django 2.0.5 on 2018-07-17 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='عنوان')),
                ('is_for_factory', models.BooleanField(default=False, verbose_name='بخش آماده سازی می باشد')),
            ],
            options={
                'verbose_name': 'بخش',
                'verbose_name_plural': 'بخش ها',
                'permissions': (('can_see_division', 'می تواند مشاهده کند'),),
            },
        ),
    ]
