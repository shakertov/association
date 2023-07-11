from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import hashlib

# Загрузка моделей
from users.models import (
	RequestUser,
	Invite,
	ExtraFieldsExpert
)

# Загрузка форм
from users.forms import (
	RequestUserForm,
	RegistrationForm,
	LoginForm
)

# Хелпер
from users.helpers import lk_redirect


User = get_user_model()


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

	link_to_invite = obj.last_name + obj.first_name + obj.email
	hash_link = hashlib.new('md5')
	hash_link.update(link_to_invite.encode())
	hash_link = hash_link.hexdigest()

	invite = Invite.objects.get_or_create(
		request=obj,
		link=hash_link
	)

	site = 'http://127.0.0.1:8000/users/reg/'
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


def registration(request, link):
	try:
		link_for_reg = Invite.objects.get(link=link)
	except Invite.DoesNotExist:
		return HttpResponseRedirect(reverse('users:login'))
	user_request = link_for_reg.request

	data_request = {
		'last_name': user_request.last_name,
		'first_name': user_request.first_name,
		'middle_name': user_request.middle_name,
		'email': user_request.email,
		'phone': user_request.phone
	}

	form = RegistrationForm(data_request)

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			# Поля основной модели email, password
			# Поля extra last_name, first_name
			# middle_name, phone, about
			fields_extra = {
				'last_name': form.cleaned_data.pop('last_name'),
				'first_name': form.cleaned_data.pop('first_name'),
				'middle_name': form.cleaned_data.pop('middle_name'),
				'phone': form.cleaned_data.pop('phone'),
				'about': form.cleaned_data.pop('about')
			}
			expert = form.save()
			fields_extra['expert'] = expert
			ExtraFieldsExpert.objects.create(**fields_extra)

			messages.add_message(
				request,
				messages.INFO,
				'Регистрация прошла успешно!')
			return HttpResponseRedirect(reverse('users:login'))

	data = {
		'form': form,
		'title': 'Регистрация эксперта',
		'action': reverse('users:registration', args=[link]),
		'button': 'Зарегистрироваться'
	}
	return render(request, 'users/request.html', data)


def login_view(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			expert = authenticate(email=email, password=password)
			if expert is not None:
				login(request, expert)

				messages.add_message(
				request,
				messages.INFO,
				'Добро пожаловать, Уважаемый ' + expert.first_name)
				return HttpResponseRedirect(reverse('pages:index'))
	data = {
		'form': form,
		'title': 'Вход в личный кабинет',
		'action': reverse('users:login'),
		'button': 'Войти в ЛК'
	}
	return render(request, 'users/request.html', data)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('users:login'))
