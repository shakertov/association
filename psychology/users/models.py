from django.db import models
from django.core.validators import validate_email


class RequestUser(models.Model):
	first_name = models.CharField(
		verbose_name='Имя',
		help_text='Введите ваше имя',
		max_length=100)
	last_name = models.CharField(
		verbose_name='Фамилия',
		help_text='Введите вашу фамилию',
		max_length=100)
	middle_name = models.CharField(
		verbose_name='Отчество',
		help_text='Введите ваше отчество',
		max_length=100)
	phone = models.CharField(
		verbose_name='Номер телефона',
		help_text='Введите ваш номер телефона',
		max_length=20)
	email = models.EmailField(
		verbose_name='Email',
		help_text='Введите ваш Email. Необходимо указывать тот, который будет использован при регистрации.',
		max_length=100)
	city = models.CharField(
		verbose_name='Город',
		help_text='Введите город, в котором хотите стать нашим представителем',
		max_length=100)
	skill = models.CharField(
		verbose_name='Область специализации',
		help_text='Введите через знак - ; - ваши навыки. Например - психология; эзотерика; и т.д.',
		max_length=255)

	class Meta:
		ordering = ['-id']
