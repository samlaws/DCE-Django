# Generated by Django 2.1.7 on 2019-03-28 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_application'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Application',
        ),
    ]