# Generated by Django 2.1.7 on 2019-04-02 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defects', '0017_auto_20190402_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.CharField(choices=[('Functional', 'Functional'), ('Performance', 'Performance'), ('Reliability and Scalability Issues', 'Reliability and Scalability Issues'), ('Security', 'Security'), ('Usability', 'Usability'), ('Compliance', 'Compliance')], default='Not Classified', max_length=20),
        ),
    ]
