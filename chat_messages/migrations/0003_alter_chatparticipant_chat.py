# Generated by Django 5.1.1 on 2024-10-24 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_messages', '0002_alter_chatparticipant_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatparticipant',
            name='chat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='chat_messages.chat'),
            preserve_default=False,
        ),
    ]