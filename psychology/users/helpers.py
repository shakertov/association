from django.http import HttpResponseRedirect
from django.urls import reverse


def lk_redirect(request):
	"""Функция перенаправляет в свой личный кабинет"""
	if not request.user.is_anonymous:
		if request.user.is_expert:
			return HttpResponseRedirect(reverse('pages:oferta'))
		if request.user.is_admin:
			return HttpResponseRedirect(reverse('pages:copyright'))
	return
