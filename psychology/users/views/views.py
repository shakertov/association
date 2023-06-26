from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
import hashlib

# Загрузка моделей
from users.models import (
	RequestUser,
	Invite
)

# Загрузка форм
from users.forms import RequestUserForm


def get_representative(request):
	"""Форма для отправки запроса на вступление в ассоциацию"""
	form = RequestUserForm()

	if request.method == 'POST':
		form = RequestUserForm(request.POST)
		if form.is_valid():
			obj = RequestUser(**form.cleaned_data)
			obj.save()
			return HttpResponseRedirect('/users/list_representative')

	data = {
		'form': form,
		'title': 'Заявка на вступление в Ассоциацию',
		'action': reverse('users:get_representative'),
		'button': 'Отправить'
	}

	return render(request, 'users/request.html', data)


def invite(request, id):
	"""
	Отправка приглашения на почтовый адрес
	1.	Формируется уникальная строка
	2.	Строка добавляется в базу и отправляется
		пользователю по Email
	3.	Строка формируется из Имени, Фамилии
	"""
	try:
		obj = RequestUser.objects.get(id=id)
	except RequestUser.DoesNotExist:
		return HttpResponse('404')

	link_to_invite = obj.last_name + obj.first_name
	hash_link = hashlib.new('md5')
	hash_link.update(link_to_invite.encode())
	hash_link = hash_link.hexdigest()

	invite = Invite.objects.get_or_create(
		request=obj,
		link=hash_link
	)

	site = 'http://127.0.0.1:8000/users/check/'
	send_mail(
		'[aaxpert] Приглашение на регистрацию',
		'Ваш HASH для вступления: ' + site + hash_link,
		'from@mailer.com',
		['to@mailer.com'],
		fail_silently=False
	)
	messages.add_message(
				request,
				messages.INFO,
				'Приглашение отправлено на почту пользователю: '
				+ obj.last_name + ' ' + obj.first_name)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
