from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Загрузка моделей
from users.models import (
	RequestUser,
	Department,
	Skill
)

# Загрузка форм
from users.forms import (
	DepartmentForm,
	SkillForm
)


def list_representative(request):
	"""Список всех заявок на вступление"""
	requests = RequestUser.objects.all()
	data = {
		'requests': requests,
		'title': 'Список заявок'
	}
	return render(request, 'users/list_requests.html', data)


def department_add(request):
	form = DepartmentForm()
	if request.method == 'POST':
		form = DepartmentForm(request.POST)
		if form.is_valid():
			city = form.cleaned_data.get('city')
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Город: ' + city + ' - добавлен в базу данных.')
			return HttpResponseRedirect(reverse('users:departments'))
	data = {
		'form': form,
		'title': 'Добавление города',
		'action': reverse('users:department_add'),
		'button': 'Добавить город'
	}
	return render(request, 'users/request.html', data)


def department_edit(request, id):
	try:
		obj = Department.objects.get(id=id)
	except Department.DoesNotExist:
		return HttpResponseRedirect(reverse('users:departments'))
	form = DepartmentForm(request.POST or None, instance=obj)
	if request.method == 'POST':
		if form.is_valid():
			city = form.cleaned_data.get('city')
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Город: ' + city + ' - отредактирован.')
			return HttpResponseRedirect(reverse('users:department_edit', args=[obj.id]))
	data = {
		'form': form,
		'title': 'Редактирование города',
		'button': 'Изменить название города'
	}
	return render(request, 'users/request.html', data)


def department_delete(request, id):
	try:
		obj = Department.objects.get(id=id)
	except Department.DoesNotExist:
		return HttpResponseRedirect(reverse('users:departments'))
	city = obj.city
	obj.delete()
	messages.add_message(
				request,
				messages.INFO,
				'Город: ' + city + ' - удалён.')
	return HttpResponseRedirect(reverse('users:departments'))


def departments(request):
	departments = Department.objects.all()
	data = {
		'departments': departments,
		'title': 'Список всех городов участников'
	}
	return render(request, 'users/departments.html', data)


def skills(request):
	return