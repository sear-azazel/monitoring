# Generated by Django 2.2.1 on 2019-06-25 15:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recognition',
            name='recognition_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
