from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Form to be used to log users in"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class UseRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)
    
    """this will provide information about the form"""
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    """clean the form field and validade it inserting a the new user"""
    def clean_email(self):
        email= self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email
    
    def clean_passord2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or not password2:
            raise ValidationError('Please confirm your password')
        
        if password1 != password2:
            raise ValidationError("Password must match")
        return password2