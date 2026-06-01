from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomerLoginForm, CustomerRegisterForm


class RoleBasedLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomerLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return reverse("admin_dashboard")

        return reverse("product_list")


def register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = CustomerRegisterForm()

    return render(request, "accounts/register.html", {
        "form": form,
    })


def logout_view(request):
    logout(request)
    return redirect("home")