from django.urls import path
from . import views


app_name = 'pages'

urlpatterns = [
	path('', views.index, name='index'),
	path('oferta/', views.oferta, name='oferta'),
	path('confidentiality/', views.confidentiality, name='confidentiality'),
	path('copyright/', views.copyright, name='copyright'),
	path('representative/', views.representative, name='representative')
]
