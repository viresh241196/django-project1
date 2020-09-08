from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileRegistrationForm(forms.ModelForm):
    savings = forms.IntegerField(label='Enter your first savings', required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['savings', 'date_of_birth', 'adharcard_number', 'profile_image', 'address', 'mobile_number']


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Enter your username', max_length=50)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'adharcard_number', 'profile_image', 'address', 'mobile_number']


class DepositForm(forms.ModelForm):
    deposit = forms.IntegerField(label='Enter the amount you want to deposit')

    class Meta:
        model = Profile
        fields = ['account_number', 'deposit']


class WithdrawForm(forms.ModelForm):
    withdraw = forms.IntegerField(label='Enter the amount you want to withdraw')

    class Meta:
        model = Profile
        fields = ['account_number', 'withdraw']


class transferForm(forms.ModelForm):
    account_number_1 = forms.IntegerField(label='form account number')
    account_number_2 = forms.IntegerField(label='to account number')
    amount = forms.IntegerField(label='amount to transfer')

    class Meta:
        model = Profile
        fields = ['account_number_1', 'account_number_2','amount']