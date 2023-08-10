from django.http import HttpResponseRedirect
from django.urls import reverse, resolve


ALLOWED_URL_FOR_ADMIN = [
	'list_representative',

	'department_add',
	'department_edit',
	'department_delete',
	'departments',

	'skill_add',
	'skill_edit',
	'skill_delete',
	'skills'
]

ALLOWED_URL_FOR_EXPERT = [
	'events',
	'event_add',
	'event_edit',
	'event_delete'
]


def lk_redirect(request):
	"""Функция перенаправляет в свой личный кабинет"""
	url_name = resolve(request.path).url_name

	if not request.user.is_anonymous:
		if request.user.is_expert:
			if url_name not in ALLOWED_URL_FOR_EXPERT:
				return HttpResponseRedirect(reverse('users:login'))
		if request.user.is_admin:
			if url_name not in ALLOWED_URL_FOR_ADMIN:
				return HttpResponseRedirect(reverse('users:login'))
	else:
		return HttpResponseRedirect(reverse('users:login'))

	return
