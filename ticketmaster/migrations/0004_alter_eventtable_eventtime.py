# Generated by Django 4.2.7 on 2023-12-03 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketmaster', '0003_eventtable_eventdate_eventtable_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtable',
            name='eventTime',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]
