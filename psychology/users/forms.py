from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import (
	RequestUser,
	Department,
	Skill
)
from events.models import (
	Event
)

User = get_user_model()


class YourOwnModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class YourOwnForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class YourOwnRegForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class RequestUserForm(YourOwnModelForm):
	class Meta:
		model = RequestUser
		fields = '__all__'


class DepartmentForm(YourOwnModelForm):
	class Meta:
		model = Department
		fields = '__all__'


class SkillForm(YourOwnModelForm):
	class Meta:
		model = Skill
		fields = '__all__'


class RegistrationForm(YourOwnRegForm):
	last_name = forms.CharField(
		label='Фамилия',
		help_text='Введите Вашу фамилию',
		max_length=100
	)
	first_name = forms.CharField(
		label='Имя',
		help_text='Введите Ваше имя',
		max_length=100
	)
	middle_name = forms.CharField(
		label='Отчество',
		help_text='Введите Ваше отчество',
		max_length=100
	)
	phone = forms.CharField(
		label='Номер телефона',
		help_text='Введите Ваш номер телефона'
	)
	about = forms.CharField(
		label='Информация об эксперте',
		help_text='Напишите о себе. '\
		'Эта информация будет предоставлена посетителю сайта. '\
		'Здесь можно описать свой опыт и образование,'\
		' виды предоставляемых услуг '\
		'и их стоимость. Заранее подготовьте текст',
		widget=forms.Textarea
	)

	class Meta:
		model = User
		fields = [
		'last_name',
		'first_name',
		'middle_name',
		'email',
		'password1',
		'password2',
		'phone',
		'about']


class LoginForm(YourOwnForm):
	email = forms.EmailField(
		label='Email',
		help_text='Введите Ваш Email, указанный при регистрации'
	)
	password = forms.CharField(
		label='Пароль',
		help_text='Введите Ваше пароль, указанный при регистрации',
		widget=forms.PasswordInput
	)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		error_message = 'Логин или пароль не совпадают'
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			raise ValidationError(error_message)
		temp_user = authenticate(
			email=email,
			password=password)
		if temp_user == None:
			raise ValidationError(error_message)
		return self.cleaned_data


class EventForm(YourOwnModelForm):
	class Meta:
		model = Event
		fields = [
			'title',
			'description',
			'city',
			'address',
			'datetime'
		]
