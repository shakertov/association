from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import hashlib
from django.core.paginator import Paginator

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

	return render(request, 'users/request_for_base.html', data)


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

	site = 'http://aexpertov.ru/users/reg/'
	send_mail(
		'[aaxpert] Приглашение на регистрацию',
		'Ваша ссылка для регистрации: ' + site + hash_link,
		'admin@aexpertov.ru',
		[obj.email],
		fail_silently=False
	)
	messages.add_message(
				request,
				messages.INFO,
				'Приглашение отправлено на почту пользователю: '
				+ obj.last_name + ' ' + obj.first_name)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def registration(request, link):
	if not request.user.is_anonymous:
		return HttpResponseRedirect(reverse('users:login'))
	try:
		link_for_reg = Invite.objects.get(link=link)
		if link_for_reg.status:
			return HttpResponseRedirect(reverse('users:login'))
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

			link_for_reg.status = True
			link_for_reg.save()

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
	return render(request, 'users/request_for_base.html', data)


def login_view(request):
	if not request.user.is_anonymous:
		if request.user.is_admin:
			return HttpResponseRedirect(reverse('users:list_representative'))
		if request.user.is_expert:
			return HttpResponseRedirect(reverse('users:events'))
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)

				messages.add_message(
				request,
				messages.INFO,
				'С возвращением!')
				if user.is_admin:
					return HttpResponseRedirect(reverse('users:list_representative'))
				if user.is_expert:
					return HttpResponseRedirect(reverse('users:events'))
				return HttpResponseRedirect(reverse('pages:index'))
	data = {
		'form': form,
		'title': 'Вход в личный кабинет',
		'action': reverse('users:login'),
		'button': 'Войти в ЛК'
	}
	return render(request, 'users/login.html', data)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('users:login'))


def reset_pass_done(request):
	messages.add_message(
		request,
		messages.INFO,
		'Проверьте почту для сброса пароля!')
	return HttpResponseRedirect(reverse('users:reset_pass'))


def pass_confirm_done(request, uidb64):
	messages.add_message(
		request,
		messages.INFO,
		'Пароль успешно установлен!')
	return HttpResponseRedirect(reverse('users:login'))


def experts(request):
	experts = User.objects.filter(role='expert')
	
	per_page = 10
	page_number = request.GET.get('page')

	paginator = Paginator(experts, per_page)
	page_obj = paginator.get_page(page_number)


	data = {
		'page_obj': page_obj
	}
	return render(request, 'experts.html', data)


def expert(request, id):
	try:
		expert = User.objects.get(id=id)
	except User.DoesNotExist:
		return HttpResponse('404')

	data = {
		'expert': expert
	}
	return render(request, 'expert.html', data)
