# Generated by Django 2.2.4 on 2021-09-29 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_team_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userseason',
            name='unc_losses',
        ),
        migrations.RemoveField(
            model_name='userseason',
            name='unc_place',
        ),
        migrations.RemoveField(
            model_name='userseason',
            name='unc_wins',
        ),
    ]
