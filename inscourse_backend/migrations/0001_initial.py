# Generated by Django 3.2 on 2021-05-01 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
    ]
