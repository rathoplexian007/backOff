# Generated by Django 3.2.9 on 2022-02-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_meeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='officials',
            name='blockchain_address',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
