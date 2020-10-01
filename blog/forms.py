from django import forms
from .models import Post, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'status',
        )

# class UserLoginForm(forms.Form):
#     username = forms.CharField(label="")
#     password = forms.CharField(label="", widget= forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password            = forms.CharField(widget= forms.PasswordInput(attrs= {'placeholder': 'Enter password here... '}))
    confirm_password    = forms.CharField(widget= forms.PasswordInput(attrs= {'placeholder': 'Confirm password... '}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password did not match!')
        return confirm_password


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget= forms.TextInput(attrs= {'readonly': 'readonly'}))
    email = forms.CharField(widget= forms.TextInput(attrs= {'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )