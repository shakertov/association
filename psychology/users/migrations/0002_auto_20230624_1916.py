# Generated by Django 3.2 on 2023-06-24 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestuser',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='city',
            field=models.CharField(help_text='Введите город, в котором хотите стать нашим представителем', max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='email',
            field=models.EmailField(help_text='Введите ваш Email. Необходимо указывать тот, который будет использован при регистрации.', max_length=100, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='first_name',
            field=models.CharField(help_text='Введите ваше имя', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='last_name',
            field=models.CharField(help_text='Введите вашу фамилию', max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='middle_name',
            field=models.CharField(help_text='Введите ваше отчество', max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='phone',
            field=models.CharField(help_text='Введите ваш номер телефона', max_length=20, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='requestuser',
            name='skill',
            field=models.CharField(help_text='Введите через знак - ; - ваши навыки. Например - психология; эзотерика; и т.д.', max_length=255, verbose_name='Область специализации'),
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=32)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.requestuser')),
            ],
            options={
                'unique_together': {('request', 'link')},
            },
        ),
    ]