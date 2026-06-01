from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "auth-input",
            "placeholder": "Nhập tên đăng nhập",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "Nhập mật khẩu",
            "autocomplete": "current-password",
        })
    )


class CustomerRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            "class": "auth-input",
            "placeholder": "Tạo tên đăng nhập",
        })
    )

    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "Nhập mật khẩu",
        })
    )

    password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "Nhập lại mật khẩu",
        })
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")