# Generated by Django 3.0.2 on 2020-05-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_index',
            field=models.BooleanField(default=False),
        ),
    ]
