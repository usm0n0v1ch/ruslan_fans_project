# Generated by Django 4.2.16 on 2024-10-01 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='app/media/icon_for_nav/profile.png', null=True, upload_to='profile_pics'),
        ),
    ]
