# Generated by Django 2.1.7 on 2019-03-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defects', '0007_article_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='classification',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
