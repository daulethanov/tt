# Generated by Django 5.0.4 on 2024-04-21 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('numbers', models.CharField(max_length=12, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('invite_profile', models.CharField(blank=True, max_length=6, null=True)),
                ('username', models.CharField(max_length=12)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]