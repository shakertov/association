from django.urls import path
from events import views


app_name = 'events'

urlpatterns = [
	path('', views.events, name='events'),
	path('id/<int:id>/', views.event, name='event')
]