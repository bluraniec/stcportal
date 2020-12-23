# from django.contrib.auth.decorators import login_required
import requests
import time
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import AuthTable, AuthTableForm, Packages

def authtable_main(request):
    """ View for rendering entries of AuthTable.
    :param request: HTTP Request
    :type request: object
    :return: View Subscribers (if authenticated) or Login Page (if not)
    """
    column_names = AuthTable._meta.get_fields()
    auth_table = reversed(AuthTable.objects.using('external').all().values())
    data = {
        "title": "Subscriber Management",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def authtable_search(request):
    """ View for searching entries of AuthTable.
    :param request: HTTP Request
    :type request: object
    :return: View Subscribers (if authenticated) or Login Page (if not)
    """
    column_names = AuthTable._meta.get_fields()
    keyword = request.GET['q']
    queries = [Q(**{'%s__icontains' % column.name: keyword}) for column in column_names]
    qs = Q()
    for query in queries:
        qs = qs | query
    auth_table = reversed(AuthTable.objects.using('external').filter(qs).values().order_by('id')[:10])
    data = {
        "title": "Subscriber Management",
        "request": request,
        "column_names": column_names,
        "auth_table": auth_table
    }
    if request.user.is_authenticated:
        messages.info(request, 'Search results for keyword: "{}"'.format(keyword))
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def authtable_add(request):
    """ View for rendering form for adding Subscriber.
    :param request: HTTP Request
    :type request: object
    :return: Add Subscriber (if authenticated) or Login Page (if not)
    """
    try:
        if request.method == 'POST':
            form = AuthTableForm(request.POST)
            if form.is_valid():
                AuthTable = form.save(commit=False)
                AuthTable.save(using='external')
                messages.success(request, 'Success! Subscriber has been added.')
                return redirect('/subscribers')
        else:
            form = AuthTableForm()
        data = {
            "title": "Add Subscriber",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Add Subscriber, given userlogin already exists in the table.")
        return redirect('/subscribers')
    except Exception as e:
        return render(request, 'home/home.html', {"title": "Error! "+str(e)})

def authtable_edit(request, subscriber_id):
    """ View for rendering form for editing details of
        existing Subscriber.
    :param request: HTTP Request
    :type request: object
    :param subscriber_id: Subscriber ID
    :type subscriber_id: str
    :return: Edit Subscriber (if authenticated) or Login Page (if not)
    """
    try:
        auth_table = AuthTable
        subscriber = auth_table.objects.using('external').get(id=subscriber_id)
        if request.method == 'POST':
            form = AuthTableForm(request.POST, instance=subscriber)
            if form.is_valid():
                auth_table = form.save(commit=False)
                auth_table.save(using='external')
                messages.success(request, 'Success! Subscriber id={} has been edited.'.format(subscriber_id))
                return redirect('/subscribers')
        else:
            form = AuthTableForm(instance=subscriber)
        data = {
            "title": "Edit Subscriber",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Edit Subscriber, this userlogin already exists in the table.")
        return redirect('/subscribers')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/subscribers')

def authtable_delete(request, subscriber_id):
    """ View for deleting existing Subscriber.
    :param request: HTTP Request
    :type request: object
    :param subscriber_id: Subscriber ID
    :type subscriber_id: str
    :return: View Subscribers (if authenticated) or Login Page (if not)
    """
    auth_table = AuthTable
    auth_table.objects.using('external').filter(id=subscriber_id).delete()
    # response = requests.get('https://<CPAR-IP>:8443/RESTAPI/service/PoD'.format(subscriber_id), auth=('admin', 'aicuser'), 
    #                         data={"parameter": "username", "value": "", "type": "with-user"})
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        messages.success(request, 'Success! Subscriber id={} has been deleted.'.format(subscriber_id))
        return redirect('/subscribers')
    else:
        return redirect('/')

def authtable_cancel(request, subscriber_id):
    print('TO_DO')
    # response = requests.get('https://<CPAR-IP>:8443/RESTAPI/service/PoD'.format(subscriber_id), auth=('admin', 'aicuser'), 
    #                         data={"parameter": "username", "value": "", "type": "with-user"})
    # if response.code == 200:
    auth_table = AuthTable
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    subscriber = auth_table.objects.using('external').filter(id=subscriber_id).update(status=0, endofsubscription=today)
    messages.success(request, 'Success! Subscriber id={} has been cancelled.'.format(subscriber_id))
    return redirect('/subscribers')
    # Example using curl:
    #    'https://<CAPR-IP>:8443/RESTAPI/service/PoD' --user 'admin:aicuser' -H 'Content-Type:application/json' --data '{"parameter":"username","value":"","type":"with-user"}'
    # AuthTable: Change intStatus field to 0 (DELETE and CANCEL, DELETE will involve as well CANCEL)
    # How to be authorized in calls to AAA and back?
    # response = requests.get('https://<CPAR-IP>:8443/RESTAPI/service/PoD'.format(subscriber_id), auth=('admin', 'aicuser'))
    # handle status codes
    # Change intStatus field to 0
    # Change endOfSubscription to today
    # REST API call (PoD - Packet of Disconnect) via requests send to AAA (using username)

def authtable_speed(request, subscriber_id):
    print('TO_DO')
    response = requests.get('https://<CPAR-IP>:8443/RESTAPI/service/CoA'.format(subscriber_id), auth=('admin', 'aicuser'), 
                            data={"parameter": "username", "value": "", "type": "with-user"})
    if response.code == 200:
        auth_table = AuthTable
        packages_table = Packages
        subscriber = auth_table.objects.using('external').get(id=subscriber_id)
        package = package_table.objects.using('external').get(Type=user.package)
        subscriber.endOfSubscription = date.today() + package.validity
        auth_table.objects.using('external').create(subscriber) # Probably prepaid_card -> dict()
        auth_table.save(using='external')
        return redirect('/')
    # Example using curl: 
    #     'https://<CAPR-IP>:8443/RESTAPI/service/CoA --user 'admin:aicuser' -H 'Content-Type:application/json' --data '{"parameter":"username","value":"","type":"with-user"}'
    # Speed change should automatically recalculate endOfSubscription day (based on call to Packages)
    # Update endOfSubscription automatically
    # REST API call (CoA - Change of Authorization) via requests send to AAA (using username)