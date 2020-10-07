from django import forms
from .models import Post, Profile, Image_post, Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'status',
            'restrict_comment',
        )

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')
    class Meta:
        model = Image_post
        fields = (
            'image',
        )

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'status',
            'restrict_comment',
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

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea(attrs= {'rows': '2', }))

    class Meta:
        model = Comment
        fields = ('content',)