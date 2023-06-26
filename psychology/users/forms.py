from django import forms
from users.models import (
	RequestUser,
	Department,
	Skill
)


class YourOwnModelForm(forms.ModelForm):
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
