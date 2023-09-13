# Generated by Django 3.2 on 2023-08-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20230810_0721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-pubdate']},
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(help_text='Введите название Вашего мероприятия', max_length=255, verbose_name='Мероприятие'),
        ),
    ]