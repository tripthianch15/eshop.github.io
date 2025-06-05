from django import forms
#from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm

#class SignupForm(forms.ModelForm):
class SignupForm(UserCreationForm):
    class Meta:
        #model = CustomUser
        model = User
        #fields = ['first_name', 'contact_number', 'email', 'password']
        fields = ['first_name', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class SigninForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput())


class OTPForm(forms.ModelForm):
    
    OTP = forms.CharField()
    class Meta:
     model = User
     fields = ['username']
     
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Confirm New Password"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user