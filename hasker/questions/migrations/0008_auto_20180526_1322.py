# Generated by Django 2.0.5 on 2018-05-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20180526_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, default=None, to='questions.Tag', verbose_name='list of tags'),
        ),
    ]
