from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Загрузка моделей
from events.models import (
	Event
)

# Загрузка форм
from users.forms import (
	EventForm,
	ProfileForm
)

# Загрузка хелпера
from users.helpers import lk_redirect

@login_required
def events(request):
	"""Список всех мероприятий эксперта"""
	response = lk_redirect(request)
	if response is not None:
		return response
	events = Event.objects.filter(expert=request.user)
	data = {
		'events': events,
		'title': 'Список мероприятий'
	}
	return render(request, 'users/expert_events.html', data)


@login_required
def event_add(request):
	response = lk_redirect(request)
	if response is not None:
		return response
	form = EventForm()
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event = form.save(commit=False)
			event.expert_id = request.user.pk
			event.save()
			messages.add_message(
				request,
				messages.INFO,
				'Мероприятие успешно добавлено!')
			return HttpResponseRedirect(reverse('users:events'))

	data = {
		'form': form,
		'title': 'Добавление мероприятия',
		'action': reverse('users:event_add'),
		'button': 'Добавить мероприятие'
	}

	return render(request, 'users/request_for_expert.html', data)

@login_required
def event_edit(request, id):
	response = lk_redirect(request)
	if response is not None:
		return response
	try:
		obj = Event.objects.get(id=id)
	except Event.DoesNotExist:
		return HttpResponseRedirect(reverse('users:events'))
	if obj.expert_id != request.user.pk:
		messages.add_message(
			request,
			messages.INFO,
			'Вы не являетесь экспертом мероприятия, к которому обращаетесь')
		return HttpResponseRedirect(reverse('users:events'))
	form = EventForm(request.POST or None, instance=obj)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Мероприятие успешно отредактировано!')
			return HttpResponseRedirect(reverse('users:event_edit', args=[obj.id]))
	data = {
		'form': form,
		'title': 'Редактирование мероприятия',
		'action': reverse('users:event_edit', args=[obj.id]),
		'button': 'Внести изменения'
	}
	return render(request, 'users/request_for_expert.html', data)

@login_required
def event_delete(request, id):
	response = lk_redirect(request)
	if response is not None:
		return response
	try:
		obj = Event.objects.get(id=id)
	except Event.DoesNotExist:
		return HttpResponseRedirect(reverse('users:events'))
	if obj.expert_id != request.user.pk:
		messages.add_message(
			request,
			messages.INFO,
			'Вы не являетесь экспертом мероприятия, к которому обращаетесь')
		return HttpResponseRedirect(reverse('users:events'))
	title = obj.title
	obj.delete()
	messages.add_message(
		request,
		messages.INFO,
		'Мероприятие: ' + title + ' - удалено.')
	return HttpResponseRedirect(reverse('users:events'))

@login_required
def profile(request):
	response = lk_redirect(request)
	if response is not None:
		return response
	user = request.user
	extra_fields = user.fields
	form = ProfileForm(request.POST or None,
		files=request.FILES or None,
		instance=extra_fields)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Профиль отредактирован')
			return HttpResponseRedirect(reverse('users:profile'))
	data = {
		'form': form,
		'title': 'Редактирование профиля',
		'action': reverse('users:profile'),
		'button': 'Внести изменения',
		'files_form': True
	}
	return render(request, 'users/request_for_expert.html', data)

@login_required
def success_chg_pass(request):
	messages.add_message(
		request,
		messages.INFO,
		'Пароль успешно изменён!')
	return HttpResponseRedirect(reverse('users:expert_chg_pass'))
