# Generated by Django 2.0.2 on 2018-02-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sm_main', '0010_statistic_info_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic_info',
            name='group_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
