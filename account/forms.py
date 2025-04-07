from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import EmailInput, PasswordInput
from django.contrib.auth import authenticate


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(
                request=self.request,
                username=username,
                password=password
            )
            
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
            
            self.user_cache = user
        
        return self.cleaned_data
