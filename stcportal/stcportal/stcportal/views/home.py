# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from ..models import User, LoginForm


def home_login(request):
    """ View for login/user authentication and rendering portal Home Page.
    :param request: HTTP Request
    :type request: object
    :return: View Home Page (if authenticated) or Login Page (if not)
    """
    if request.user.is_authenticated:
        return render(request, 'home/home.html', {'title': 'Welcome to the Official Saudi Telecom Broadband Support Portal.'})
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # MFA Placeholder for the future
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not user.is_active:
                    form.error = "This account is inactive."
                else:
                    return render(request, 'home/home.html', {'title': 'Welcome to the Official Saudi Telecom Broadband Support Portal.'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def home_logout(request):
    """ View for logout and rendering portal Login Page.
    :param request: HTTP Request
    :type request: object
    :return: View Login Page (if succesfuly logged out)
    """
    logout(request)
    return redirect('/')