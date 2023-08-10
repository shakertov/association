from django.db import models
from django.contrib.auth import get_user_model

from users.models import Department


User = get_user_model()


class Event(models.Model):
	expert = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='events')
	title = models.CharField(
		verbose_name='Мероприятие',
		help_text='Введите название Вашего мероприятия',
		max_length=255)
	description = models.TextField(
		verbose_name='Вся информация о событии',
		help_text='Введите подробное описание мероприятия, заранее подготовьте текст')
	city = models.ForeignKey(
		Department,
		verbose_name='Город',
		help_text='Выберите город, в котором будет проходить мероприятие',
		on_delete=models.CASCADE,
		related_name='events')
	address = models.CharField(
		verbose_name='Адрес',
		help_text='Введите адрес, где будет проходить мероприятие без указания города',
		max_length=255)
	pubdate = models.DateTimeField(
		auto_now=False,
		auto_now_add=True)
	datetime = models.DateTimeField(
		verbose_name='Дата проведения',
		help_text='Введите дату в формате: дд.мм.гггг чч:мм:сс',
		auto_now=False,
		auto_now_add=False)

	class Meta:
		ordering = ['-pubdate']
