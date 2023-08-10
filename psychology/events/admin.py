from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
	list_display = (
		'title',
		'description',
		'pubdate',
		'datetime',
		'city'
	)
	search_fields = (
		'title',
		'city',
		'datetime',
	)

admin.site.register(Event, EventAdmin)
