# Generated by Django 4.0.6 on 2022-08-28 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0015_remove_calevent_private_eventgroup_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calevent',
            name='isAnniv',
            field=models.BooleanField(default=False, help_text='Will show the # of years since event.'),
        ),
    ]