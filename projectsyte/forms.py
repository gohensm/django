from django import forms
from .models import Post, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'bio']

class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField(label='Avatar')