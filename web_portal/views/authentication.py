import logging
from django.views import View
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, password_validation, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from custom_admin.model_classes import CustomUser

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(
        max_length=100, label="Password", widget=forms.PasswordInput)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, 'login.html', {
            'form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Debugging: Log the username and password being used for authentication
            logger.debug(f"Attempting to authenticate user '{username}' with password '{password}'")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f"User '{username}' logged in successfully.")
                    return redirect('home')
                else:
                    logger.warning(f"Failed login attempt for inactive user '{username}'.")
                    form.add_error('username', 'This account is inactive.')
            else:
                logger.warning(f"Failed login attempt for unknown user '{username}'.")
                form.add_error('password', 'Invalid username or password.')

        logger.error(f"Form data invalid: {form.errors}")
        return render(request, 'login.html', {'form': form})


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(
        max_length=100, label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        max_length=100, label="Password", widget=forms.PasswordInput)


class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = RegistrationForm()
        return render(request, 'registration.html', {
            'form': form
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                form.add_error('password', error)

            if (password != password_confirm):
                form.add_error('password', 'Passwords do not match.')

            if not form.is_valid():
                return render(request, 'registration.html', {'form': form})

            try:
                # Create user
                hashed_password = make_password(password) 
                user_record = CustomUser.objects.create(
                    username=username,
                    password=hashed_password
                )
                return HttpResponseRedirect('/')
            except Exception as e:
                form.add_error(
                    'password', 'Failed to create user: {}'.format(str(e)))
                return render(request, 'registration.html', {
                    'form': form
                })

        return render(request, 'registration.html', {
            'form': form
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect('/')
