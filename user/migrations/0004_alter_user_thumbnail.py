# Generated by Django 3.2.6 on 2021-10-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='thumbnail',
            field=models.CharField(blank=True, default='default_profile.jpg', max_length=256, null=True),
        ),
    ]
