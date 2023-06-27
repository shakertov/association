from django.urls import path
from users.views import (
	views,
	lk_admin,
	lk_expert
)


app_name = 'users'

urlpatterns = [
	# Авторизация
	path('get_representative/',
		views.get_representative,
		name='get_representative'),
	path('invite/<int:id>/',
		views.invite,
		name='invite'),
	path('reg/<str:link>',
		views.registration,
		name='registration'),
	path('login/',
		views.login_view,
		name='login'),
	path('logout/',
		views.logout_view,
		name='logout'),

	# Личный кабинет администратора
	path('list_representative/',
		lk_admin.list_representative,
		name='list_representative'),

	path('department/add/',
		lk_admin.department_add,
		name='department_add'),
	path('department/edit/<int:id>/',
		lk_admin.department_edit,
		name='department_edit'),
	path('department/delete/<int:id>/',
		lk_admin.department_delete,
		name='department_delete'),
	path('departments/',
		lk_admin.departments,
		name='departments'),

	path('skill/add/',
		lk_admin.skill_add,
		name='skill_add'),
	path('skill/edit/<int:id>/',
		lk_admin.skill_edit,
		name='skill_edit'),
	path('skill/delete/<int:id>/',
		lk_admin.skill_delete,
		name='skill_delete'),
	path('skills/',
		lk_admin.skills,
		name='skills')
]
