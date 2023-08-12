from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager


EXPERT = 'expert'
ADMIN = 'admin'
ROLES = [
	(EXPERT, 'expert'),
	(ADMIN, 'admin')
]

class CustomUser(AbstractUser):
	"""Реализация использования email в качестве имени пользователя"""
	username = None
	email = models.EmailField(
		verbose_name='Email',
		help_text='Введите ваш Email. Он будет использован как логин для входа.',
		max_length=255,
		unique = True
	)
	role = models.CharField(
		verbose_name='Роль пользователя',
		max_length=20,
		default=EXPERT,
		choices=ROLES
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	@property
	def is_expert(self):
		return self.role == EXPERT

	@property
	def is_admin(self):
		return self.role == ADMIN

	def __str__(self):
		return self.email


class ExtraFieldsExpert(models.Model):
	expert = models.OneToOneField(
		'CustomUser',
		on_delete=models.CASCADE,
		related_name='fields'
	)
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
	about = models.TextField(
		verbose_name='Обо мне',
		help_text='Расскажите о себе'
	)
	avatar = models.ImageField(
		verbose_name='Фото профиля',
		help_text='Загрузите Ваше фото, которое будет представлено посетителям',
		blank=True,
		upload_to='avatars')


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


class Invite(models.Model):
	request = models.OneToOneField(
		'RequestUser',
		on_delete=models.CASCADE,
		related_name='invite')
	link = models.CharField(
		max_length=32)
	status = models.BooleanField(
		default=False
		)

	class Meta:
		unique_together = ('request', 'link', )


class Department(models.Model):
	city = models.CharField(
		verbose_name='Название города',
		help_text='Введите название города, в котором имеются Ваши представители',
		max_length=100)

	def __str__(self):
		return self.city

	class Meta:
		ordering = ['city']


class Skill(models.Model):
	skill = models.CharField(
		verbose_name='Область специализации',
		help_text='Введите название специализации',
		max_length=100)

	class Meta:
		ordering = ['skill']
