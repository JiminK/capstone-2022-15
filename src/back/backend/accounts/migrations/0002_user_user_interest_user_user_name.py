# Generated by Django 4.0.3 on 2022-03-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_interest',
            field=models.TextField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default=False, max_length=30),
        ),
    ]
