# Generated by Django 5.0.4 on 2024-04-21 10:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shartnoma_app', '0002_alter_shartnoma_options_remove_shartnoma_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shartnoma',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
