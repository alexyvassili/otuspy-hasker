# Generated by Django 2.0.5 on 2018-06-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_auto_20180601_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.TextField(default='42'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='tagword',
            field=models.CharField(default=42, max_length=64),
            preserve_default=False,
        ),
    ]
