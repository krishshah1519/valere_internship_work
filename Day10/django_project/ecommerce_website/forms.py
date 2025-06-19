
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()


class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'dob', 'gender', 'phone_number']


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)


        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
