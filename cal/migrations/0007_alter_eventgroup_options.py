# Generated by Django 4.0.6 on 2022-08-28 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0006_alter_eventgroup_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventgroup',
            options={'ordering': ['name']},
        ),
    ]
