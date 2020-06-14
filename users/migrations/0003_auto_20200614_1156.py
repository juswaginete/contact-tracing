# Generated by Django 3.0.7 on 2020-06-14 11:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_time', models.TimeField(default=datetime.time(8, 0))),
                ('end_time', models.TimeField(default=datetime.time(17, 0))),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='service_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_schedule', to='users.ServiceSchedule'),
        ),
    ]