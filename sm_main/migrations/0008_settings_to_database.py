# Generated by Django 2.0.2 on 2018-02-25 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sm_main', '0007_auto_20180224_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='to_database',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]