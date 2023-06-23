from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
	path('get_representative/',
		views.get_representative,
		name='get_representative')
]
