# Generated by Django 3.2 on 2023-06-24 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_invite_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invite', to='users.requestuser'),
        ),
    ]
