# Generated by Django 5.0.4 on 2024-04-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EskizBearerToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='EskizAuthEmailAndToken',
        ),
    ]
