# Generated by Django 2.0.5 on 2018-05-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20180528_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
