# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
import base64
from datetime import date
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
# from ..models import CafeCards, CafeCardsForm, Packages

# For testing
from ..models import AuthTable, AuthTableForm

def cafecards_main(request):
    """ View for rendering entries of Cafe Cards.
    :param request: HTTP Request
    :type request: object
    :return: View Cafe Cards (if authenticated) or Login Page (if not)
    """
    column_names = AuthTable._meta.get_fields()
    auth_table = AuthTable.objects.using('external').all().filter(accounttype='Cafe').values().order_by('id')[:10]
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

def cafecards_search(request):
    """ View for searching entries of Cafe Cards.
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
    auth_table = AuthTable.objects.using('external').filter(qs).values().order_by('id')[:10]
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

def cafecards_add(request):
    """ View for rendering form for adding Cafe Card.
    :param request: HTTP Request
    :type request: object
    :return: Add Cafe Card (if authenticated) or Login Page (if not)
    """
    if request.method == 'POST':
        form = AuthTableForm(request.POST)
        if form.is_valid():
            AuthTable = form.save(commit=False)
            AuthTable.save(using='external')
    else:
        form = AuthTableForm()
    data = {
        "title": "Add Cafe Card",
        "request": request,
        "form": form
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def cafecards_edit(request, card_id):
    """ View for rendering form for editing details of
        existing Cafe Card.
    :param request: HTTP Request
    :type request: object
    :param card_id: Cafe Card ID
    :type card_id: str
    :return: Edit Cafe Card (if authenticated) or Login Page (if not)
    """
    auth_table = AuthTable
    cafe_card = auth_table.objects.using('external').get(id=card_id)
    if request.method == 'POST':
        form = AuthTableForm(request.POST, instance=cafe_card)
        if form.is_valid():
            auth_table = form.save(commit=False)
            auth_table.save(using='external')
    else:
        form = AuthTableForm(instance=cafe_card)
    data = {
        "title": "Edit Cafe Card",
        "request": request,
        "form": form
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def cafecards_delete(request, card_id):
    """ View for deleting existing Cafe Card.
    :param request: HTTP Request
    :type request: object
    :param card_id: Cafe Card ID
    :type card_id: str
    :return: View Cafe Cards (if authenticated) or Login Page (if not)
    """
    auth_table = AuthTable
    auth_table.objects.using('external').filter(id=card_id).delete()
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        return redirect('/cafe')
    else:
        return redirect('/')

def cafecards_cancel(request, subscriber_id):
    print('TO_DO')
    # response = requests.get('https://<CPAR-IP>:8443/RESTAPI/service/PoD'.format(subscriber_id), auth=('admin', 'aicuser'), 
    #                         data={"parameter": "username", "value": "", "type": "with-user"})
    # if response.code == 200:
    auth_table = AuthTable
    today = time.strftime('%Y-%m-%d %H:%M:%S')
    subscriber = auth_table.objects.using('external').filter(id=subscriber_id).update(status=0, endofsubscription=today)
    return redirect('/cafe')

@csrf_exempt
def cafecards_activate(request):
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
    username = decoded_credentials[0]
    password = decoded_credentials[1]
    user_auth = authenticate(username=username, password=password)
    if user_auth is not None:
        login(request, user_auth)
        subscriber = json.loads(request.body.decode('utf-8'))['username']
        auth_table = AuthTable
        try:
            today = date.today().strftime("%b-%d-%Y")
            user = auth_table.objects.using('external').filter(username=subscriber).update(endofsubscription=today)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)
    """
    TO BE VALIDATED:
    #### 1. Is username unique to provide in the request to AuthTable?
    #### 2. Which field to retrieve from AuthTable - Package?
    #### 3. Which field to retrieve from Package table - Promodays? And what identifies package type - Type?
    #### 4. Which field in AuthTable is for date of activation?
    """
    ## Prereq: Expose REST API to be called from AAA (http://localhost/cafe/activate/<user_id>)
    ## Get record for given username from AuthTable (grab user package_name parameter)
    # auth_table = AuthTable
    # user = auth_table.objects.using('external').get(id=user_id)
    ## Query Package table with package_name parameter to retrieve validity
    # package_table = Packages
    # package = package_table.objects.using('external').get(Type=user.package)
    ## Based on retrieved validity - update endOfSubscription date for given username in AuthTable
    ## Update other fields: speed, date of activation (set to today)
    # user.endOfSubscription = datetime.date.today() + package.Promodays
    # user.speed = package.Speed
    # user.data_of_activation = datetime.date.today()
    # user.save(update_fields=['endOfSubscription', 'speed', 'date_of_activation'])
