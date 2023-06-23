from django.contrib import admin
from .models import RequestUser


class RequestUserAdmin(admin.ModelAdmin):
	list_display = (
		'last_name',
		'first_name',
		'phone',
		'city',
		'skill'
	)
	search_fields = (
		'last_name',
		'first_name',
		'middle_name',
	)

admin.site.register(RequestUser, RequestUserAdmin)
