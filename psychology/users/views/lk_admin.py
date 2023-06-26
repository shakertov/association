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
		'action': reverse('users:department_edit'),
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


def skill_add(request):
	form = SkillForm()
	if request.method == 'POST':
		form = SkillForm(request.POST)
		if form.is_valid():
			skill = form.cleaned_data.get('skill')
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Направление: ' + skill + ' - добавлено в базу данных.')
			return HttpResponseRedirect(reverse('users:skills'))
	data = {
		'form': form,
		'title': 'Добавление специализации',
		'action': reverse('users:skill_add'),
		'button': 'Добавить навык'
	}
	return render(request, 'users/request.html', data)


def skill_edit(request, id):
	try:
		obj = Skill.objects.get(id=id)
	except Skill.DoesNotExist:
		return HttpResponseRedirect(reverse('users:skill_edit'))
	form = SkillForm(request.POST or None, instance=obj)
	if request.method == 'POST':
		if form.is_valid():
			skill = form.cleaned_data.get('skill')
			form.save()
			messages.add_message(
				request,
				messages.INFO,
				'Навык: ' + skill + ' - отредактирован.')
			return HttpResponseRedirect(reverse('users:skill_edit', args=[obj.id]))
	data = {
		'form': form,
		'title': 'Редактирование навыка',
		'action': reverse('users:skill_edit', args=[obj.id]),
		'button': 'Изменить навык'
	}
	return render(request, 'users/request.html', data)


def skill_delete(request, id):
	try:
		obj = Skill.objects.get(id=id)
	except Skill.DoesNotExist:
		return HttpResponseRedirect(reverse('users:skills'))
	skill = obj.skill
	obj.delete()
	messages.add_message(
				request,
				messages.INFO,
				'Навык: ' + skill + ' - удалён.')
	return HttpResponseRedirect(reverse('users:skills'))


def skills(request):
	skills = Skill.objects.all()
	data = {
		'skills': skills,
		'title': 'Список всех направлений деятельности экспертов'
	}
	return render(request, 'users/skills.html', data)