# Generated by Django 4.0.6 on 2022-08-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0012_alter_calevent_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgroup',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
