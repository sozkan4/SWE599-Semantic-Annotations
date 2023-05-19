from django import forms
from .models import Annotation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['content', 'annotation_type', 'target']
