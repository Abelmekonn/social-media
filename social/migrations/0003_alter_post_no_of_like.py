# Generated by Django 4.2.5 on 2023-12-06 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='no_of_like',
            field=models.IntegerField(default=0),
        ),
    ]
