from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple

# User profile model fields
class UserProfileForm(forms.ModelForm):
    tech_stack = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'list-unstyled d-flex flex-wrap'}),
        required=False
    )
    github = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)
    phone = forms.CharField(max_length=15, required=False)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ['about','tech_stack', 'github', 'linkedin', 'phone', 'location']

# signup form from user model
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')


#forms to add projects
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','industry','founder','cofounders_needed']
        exclude = ['founder']

# project request form
class RequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['user', 'message','project']
        exclude = ['user', 'project']

# project request form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['user', 'message','to']
        exclude = ['user', 'to']
        