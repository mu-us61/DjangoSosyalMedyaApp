# Generated by Django 5.2 on 2025-04-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='default_profile.png', null=True, upload_to='profilePictures/'),
        ),
    ]
