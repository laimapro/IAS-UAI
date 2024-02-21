import uuid

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import User, Participant, Manager, Coordinator


# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label='Email / Username')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class ParticipantCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['name'].widget.attrs.update({'autofocus': True})

    class Meta(UserCreationForm.Meta):
        model = Participant
        fields = ('email', 'name', 'password1', 'password2', 'i_agree')


class CoordinatorCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['name'].widget.attrs.update({'autofocus': True})

    class Meta(UserCreationForm.Meta):
        model = Coordinator
        fields = ('email', 'name', 'password1', 'password2', 'i_agree', )


class ManagerCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['name'].widget.attrs.update({'autofocus': True})

    class Meta(UserCreationForm.Meta):
        model = Manager
        fields = ('cnpj', 'address', 'email', 'name', 'password1', 'password2', 'i_agree', 'language', )
