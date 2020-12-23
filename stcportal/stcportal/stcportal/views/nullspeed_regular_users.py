# from django.contrib.auth.decorators import login_required
import datetime, datedelta
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from ..models import NullSpeedRegularUsers, NullSpeedRegularUsersForm, AuthTable, AuthTableForm, Packages


def nullspeed_regular_users_main(request):
    """ View for rendering entries of Null Speed Regular Users.
    :param request: HTTP Request
    :type request: object
    :return: View Null Speed Regular Users (if aunthenticated) or Login Page (if not)
    """
    column_names = NullSpeedRegularUsers._meta.get_fields()
    nullspeed_regular_users = NullSpeedRegularUsers.objects.using('external').all().values().order_by('id')[:10]
    data = {
        "title": "Null Speed Regular Users",
        "request": request,
        "column_names": column_names,
        "nullspeed_regular_users": nullspeed_regular_users
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def nullspeed_regular_users_search(request):
    """ View for searching entries of Null Speed Regular Users.
    :param request: HTTP Request
    :type request: object
    :return: View Null Speed Regular Users (if authenticated) or Login Page (if not)
    """
    column_names = NullSpeedRegularUsers._meta.get_fields()
    keyword = request.GET['q']
    queries = [Q(**{'%s__icontains' % column.name: keyword}) for column in column_names]
    qs = Q()
    for query in queries:
        qs = qs | query
    nullspeed_regular_users = NullSpeedRegularUsers.objects.using('external').filter(qs).values().order_by('id')[:10]
    data = {
        "title": "Null Speed Regular Users",
        "request": request,
        "column_names": column_names,
        "nullspeed_regular_users": nullspeed_regular_users
    }
    if request.user.is_authenticated:
        messages.info(request, 'Search results for keyword: "{}"'.format(keyword))
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def nullspeed_regular_users_add(request):
    """ View for rendering form for adding Null Speed Regular Users.
    :param request: HTTP Request
    :type request: object
    :return: Add Null Speed Regular User (if aunthenticated) or Login Page (if not)
    """
    try:
        if request.method == 'POST':
            form = NullSpeedRegularUsersForm(request.POST)
            if form.is_valid():
                NullSpeedRegularUsers = form.save(commit=False)
                NullSpeedRegularUsers.save(using='external')
                messages.success(request, 'Success! NullSpeed Regular User has been added.')
                return redirect('/nullspeed/regular-users/')
        else:
            form = NullSpeedRegularUsersForm()
        data = {
            "title": "Add Null Speed Regular User",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Add NullSpeed Regular User, given userlogin already exists in the table.")
        return redirect('/nullspeed/regular-users')
    except Exception as e:
        return render(request, 'home/home.html', {"title": "Error! "+str(e)})

def nullspeed_regular_users_edit(request, user_id):
    """ View for rendering form for editing details of
        existing Null Speed Regular Users.
    :param request: HTTP Request
    :type request: object
    :param user_id: Null Speed Regular User ID
    :type user_id: str
    :return: Edit Null Speed Regular User (if aunthenticated) or Login Page (if not)
    """
    try:
        nullspeed_regular_users = NullSpeedRegularUsers
        user = nullspeed_regular_users.objects.using('external').get(id=user_id)
        if request.method == 'POST':
            form = AuthTableForm(request.POST, instance=user)
            if form.is_valid():
                nullspeed_regular_users = form.save(commit=False)
                nullspeed_regular_users.save(using='external')
                messages.success(request, 'Success! NullSpeed Regular User id={} has been edited.'.format(user_id))
                return redirect('/nullspeed/regular-users/')
        else:
            form = NullSpeedRegularUsersForm(instance=user)
        data = {
            "title": "Edit Null Speed Regular User",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Edit NullSpeed Regular User, this userlogin already exists in the table.")
        return redirect('/nullspeed/regular-users')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/nullspeed/regular-users')

def nullspeed_regular_users_delete(request, user_id):
    """ View for deleting existing Null Speed Regular User.
    :param request: HTTP Request
    :type request: object
    :param user_id: Null Speed Regular User ID
    :type user_id: str
    :return: View Prepaid (if aunthenticated) or Login Page (if not)
    """
    nullspeed_regular_users = NullSpeedRegularUsers
    nullspeed_regular_users.objects.using('external').filter(id=user_id).delete()
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        messages.success(request, 'Success! NullSpeed Regular User id={} has been deleted.'.format(user_id))
        return redirect('/nullspeed/regular-users')
    else:
        return redirect('/')

def nullspeed_regular_users_activate(request, user_id):
    """ View for moving entry from Null Speed Regular Users to AuthTable.
    :param request: HTTP Request
    :type request: object
    :param user_id: Null Speed Regular User ID
    :type user_id: str
    :return: View AuthTable (if aunthenticated) or Login Page (if not)
    """
    try:
        auth_table, packages, nullspeed_regular_users = AuthTable, Packages, NullSpeedRegularUsers
        nullspeed_regular_user = nullspeed_regular_users.objects.using('external').get(id=user_id)
        nullspeed_regular_user.id = None
        package = packages.objects.using('external').get(TypeID=nullspeed_regular_user.typeid)
        endofsubscription = datetime.datetime.now().replace(microsecond=0) + datedelta.datedelta(months=int(package.billperiod))
        auth_table.objects.using('external').create(userlogin=nullspeed_regular_user.userlogin, 
                                                    accounttype="null-regular", status=1, 
                                                    endofsubscription=endofsubscription)
        nullspeed_regular_users.objects.using('external').filter(id=user_id).delete()
        messages.success(request, 'NullSpeed Regular User id={}, userlogin={} has been activated.'.format(user_id, nullspeed_regular_user.userlogin))
        return redirect('/subscribers')
    except NullSpeedRegularUsers.DoesNotExist:
        messages.error(request, "Error! Unable to find NullSpeed Regular User with choosen id {}".format(user_id))
        return redirect('/nullspeed/regular-users')
    except Packages.DoesNotExist:
        messages.error(request, 'Error! Unable to find TypeID of the Package that was assigned to choosen NullSpeed Regular User!')
        return redirect('/nullspeed/regular-users')
    except IntegrityError:
        messages.error(request, "Error! Could not Activate NullSpeed Regular User for userlogin='{}', entry already exists in the AuthTable.".format(nullspeed_regular_user.userlogin))
        return redirect('/nullspeed/regular-users')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/nullspeed/regular-users')