from django import forms
from .models import RequestUser


class YourOwnModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class RequestUserForm(YourOwnModelForm):

	class Meta(YourOwnModelForm):
		model = RequestUser
		fields = '__all__'