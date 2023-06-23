from django.shortcuts import render
from django.http import HttpResponse

# Загрузка моделей
from .models import RequestUser

# Загрузка форм
from .forms import RequestUserForm


def get_representative(request):
	form = RequestUserForm()

	if request.method == 'POST':
		form = RequestUserForm(request.POST)
		if form.is_valid():
			obj = {
				'first_name':form.cleaned_data['first_name'],
				'last_name':form.cleaned_data['last_name'],
				'middle_name':form.cleaned_data['middle_name'],
				'email':form.cleaned_data['email'],
				'city':form.cleaned_data['city'],
				'phone':form.cleaned_data['phone'],
				'skill':form.cleaned_data['skill']
			}
			return HttpResponse(str(obj))

	data = {
		'form': form,
		'title': 'Заявка на вступление в Ассоциацию'
	}

	return render(request, 'users/request.html', data)