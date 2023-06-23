from django.shortcuts import render


def index(request):
	"""Главная страница, базовый лендинг"""
	return render(request, 'pages/index.html')

def oferta(request):
	"""Страница с офертой"""
	return render(request, 'pages/oferta.html')

def confidentiality(request):
	"""Страница конфиденциальности"""
	return render(request, 'pages/confidentiality.html')

def copyright(request):
	"""Авторские права"""
	return render(request, 'pages/copyright.html')

def representative(request):
	"""Представительства"""
