from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, views, authenticate, login, logout
from .forms import LoginForm
from .models import AuthTable, User
from .forms import AuthTableForm
from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
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

def logout_view(request):
    logout(request)
    return redirect('/')

# def subscriber_management(request):
#     column_names = AuthTable._meta.get_fields()
#     auth_table = AuthTable.objects.using('external').all().values()
#     data = {
#         "title": "Subscriber Management",
#         "request": request,
#         "column_names": column_names,
#         "auth_table": auth_table
#     }
#     if request.user.is_authenticated:
#         return render(request, 'home/home.html', data)
#     else:
#         return redirect('/')

# def subscriber_management_add(request):
#     if request.method == 'POST':
#         form = AuthTableForm(request.POST)
#         if form.is_valid():
#             AuthTable = form.save(commit=False)
#             AuthTable.save(using='external')
#     else:
#         form = AuthTableForm()
#     data = {
#         "title": "Subscriber Management - Add Subscriber",
#         "request": request,
#         "form": form
#     }
#     if request.user.is_authenticated:
#         return render(request, 'home/home.html', data)
#     else:
#         return redirect('/')

# def subscriber_management_edit(request, subscriber_id):
#     auth_table = AuthTable
#     subscriber = auth_table.objects.using('external').get(id=subscriber_id)
#     if request.method == 'POST':
#         form = AuthTableForm(request.POST, instance=subscriber)
#         if form.is_valid():
#             auth_table = form.save(commit=False)
#             auth_table.save(using='external')
#     else:
#         form = AuthTableForm(instance=subscriber)
#     data = {
#         "title": "Subscriber Management - Edit Subscriber",
#         "request": request,
#         "form": form
#     }
#     if request.user.is_authenticated:
#         return render(request, 'home/home.html', data)
#     else:
#         return redirect('/')

# def subscriber_management_delete(request, subscriber_id):
#     auth_table = AuthTable
#     auth_table.objects.using('external').filter(id=subscriber_id).delete()
#     data = {
#         "request": request
#     }
#     if request.user.is_authenticated:
#         return redirect('/subscribers')
#     else:
#         return redirect('/')

def null_speed(request):
    column_names = AuthTable._meta.get_fields()
    auth_table = AuthTable.objects.using('external').all().values()
    data = {
        "title": "Null Speed",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def prepaid(request):
    column_names = AuthTable._meta.get_fields()
    auth_table = AuthTable.objects.using('external').all().values()
    data = {
        "title": "Prepaid Cards",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def cafe(request):
    column_names = AuthTable._meta.get_fields()
    auth_table = AuthTable.objects.using('external').all().values()
    data = {
        "title": "Cafe Cards",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def packages(request):
    column_names = AuthTable._meta.get_fields()
    auth_table = AuthTable.objects.using('external').all().values()
    data = {
        "title": "Packages",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

# def reporting_and_monitoring(request):
#     users = User.objects.all()

#     if request.method == 'GET':
#         search_keyword = request.GET.get('search_box', None)

#         if search_keyword is not None:
#             users = User.objects.filter(email__icontains=search_keyword)

#         data = {
#             "title": "Reporting and Monitoring",
#             "request": request,
#             "response": users
#         }
#         if request.user.is_authenticated:
#             return render(request, 'home/home.html', data)
#         else:
#             return redirect('/')

