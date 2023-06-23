from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Загрузка моделей
from .models import RequestUser

# Загрузка форм
from .forms import RequestUserForm


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
		'title': 'Заявка на вступление в Ассоциацию'
	}

	return render(request, 'users/request.html', data)


def list_representative(request):
	"""Список всех заявок на вступление"""
	requests = RequestUser.objects.all()
	data = {
		'requests': requests,
		'title': 'Список заявок'
	}
	return render(request, 'users/list_requests.html', data)


