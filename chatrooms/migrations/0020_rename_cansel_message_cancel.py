# Generated by Django 3.2 on 2023-05-25 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0019_message_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='cansel',
            new_name='cancel',
        ),
    ]
