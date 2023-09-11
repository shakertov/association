from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from events.models import Event
from django.core.paginator import Paginator
import datetime
import pytz


def events(request):
	# Часовой пояс и время для фильтра
	tz_moscow = pytz.timezone('Europe/Moscow')
	dt = datetime.datetime.now(tz_moscow)

	events = Event.objects.filter(datetime__gte=dt).order_by('datetime')
	
	per_page = 10
	page_number = request.GET.get('page')

	paginator = Paginator(events, per_page)
	page_obj = paginator.get_page(page_number)


	data = {
		'page_obj': page_obj
	}
	return render(request, 'events.html', data)


def event(request, id):
	try:
		event = Event.objects.get(id=id)
	except Event.DoesNotExist:
		return HttpResponse('404')

	data = {
		'event': event
	}

	return render(request, 'event.html', data)
