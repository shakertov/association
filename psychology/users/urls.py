from django.urls import path
from users.views import (
	views,
	lk_admin,
	lk_expert
)
from django.contrib.auth import views as a_views
from users.forms import (
	YourOwnChangePassForm
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
		name='skills'),
	path('just/',
		lk_admin.just,
		name='just12'),

	# Личный кабинет эксперта
	path('events/',
		lk_expert.events,
		name='events'),
	path('events/add/',
		lk_expert.event_add,
		name='event_add'),
	path('events/edit/<int:id>/',
		lk_expert.event_edit,
		name='event_edit'),
	path('events/delete/<int:id>/',
		lk_expert.event_delete,
		name='event_delete'),

	path('profile/',
		lk_expert.profile,
		name='profile'),
	path('expert_chg_pass/',
		a_views.PasswordChangeView.as_view(
			template_name='users/chg_pass_expert.html',
			form_class=YourOwnChangePassForm,
			success_url='done'),
		name='expert_chg_pass'),
	path('expert_chg_pass/done/',
		lk_expert.success_chg_pass,
		name='success_chg_pass')
]
