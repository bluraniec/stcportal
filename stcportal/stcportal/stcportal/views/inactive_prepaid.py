# from django.contrib.auth.decorators import login_required
import datetime, datedelta
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from ..models import InactivePrepaid, InactivePrepaidForm, AuthTable, AuthTableForm, Packages


def inactive_prepaid_main(request):
    """ View for rendering entries of Inactive Prepaid Cards.
    :param request: HTTP Request
    :type request: object
    :return: View Inactive Prepaid (if aunthenticated) or Login Page (if not)
    """
    column_names = InactivePrepaid._meta.get_fields()
    inactive_prepaid_cards = InactivePrepaid.objects.using('external').all().values().order_by('id')[:10]
    data = {
        "title": "Inactive Prepaid Cards",
        "request": request,
        "column_names": column_names,
        "inactive_prepaid_cards": inactive_prepaid_cards
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def inactive_prepaid_search(request):
    """ View for searching entries of Inactive Prepaid Cards.
    :param request: HTTP Request
    :type request: object
    :return: View Inactive Prepaid (if authenticated) or Login Page (if not)
    """
    column_names = InactivePrepaid._meta.get_fields()
    keyword = request.GET['q']
    queries = [Q(**{'%s__icontains' % column.name: keyword}) for column in column_names]
    qs = Q()
    for query in queries:
        qs = qs | query
    inactive_prepaid_cards = InactivePrepaid.objects.using('external').filter(qs).values().order_by('id')[:10]
    data = {
        "title": "Inactive Prepaid Cards",
        "request": request,
        "column_names": column_names,
        "inactive_prepaid_cards": inactive_prepaid_cards
    }
    if request.user.is_authenticated:
        messages.info(request, 'Search results for keyword: "{}"'.format(keyword))
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def inactive_prepaid_add(request):
    """ View for rendering form for adding Inactive Prepaid Card.
    :param request: HTTP Request
    :type request: object
    :return: Add Prepaid (if aunthenticated) or Login Page (if not)
    """
    try:
        if request.method == 'POST':
            form = InactivePrepaidForm(request.POST)
            if form.is_valid():
                InactivePrepaid = form.save(commit=False)
                InactivePrepaid.save(using='external')
                messages.success(request, 'Success! Inactive Prepaid Card has been added.')
                return redirect('/prepaid')
        else:
            form = InactivePrepaidForm()
        data = {
            "title": "Add Prepaid Card",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Add Inactive Prepaid Card, given userlogin already exists in the table.")
        return redirect('/prepaid')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/prepaid')

def inactive_prepaid_edit(request, card_id):
    """ View for rendering form for editing details of
        existing Inactive Prepaid Card.
    :param request: HTTP Request
    :type request: object
    :param card_id: Inactive Prepaid Card ID
    :type card_id: str
    :return: Edit Prepaid (if aunthenticated) or Login Page (if not)
    """
    try:
        inactive_prepaid_cards = InactivePrepaid
        inactive_prepaid_card = inactive_prepaid_cards.objects.using('external').get(id=card_id)
        if request.method == 'POST':
            form = InactivePrepaidForm(request.POST, instance=inactive_prepaid_card)
            if form.is_valid():
                inactive_prepaid_cards = form.save(commit=False)
                inactive_prepaid_cards.save(using='external')
                messages.success(request, 'Success! Inactive Prepaid Card id={} has been edited.'.format(card_id))
                return redirect('/prepaid')
        else:
            form = InactivePrepaidForm(instance=inactive_prepaid_card)
        data = {
            "title": "Edit Prepaid Card",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Edit Inactive Prepaid Card, this userlogin already exists in the table.")
        return redirect('/prepaid')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/prepaid')

def inactive_prepaid_delete(request, card_id):
    """ View for deleting existing Inactive Prepaid Card.
    :param request: HTTP Request
    :type request: object
    :param card_id: Inactive Prepaid Card ID
    :type card_id: str
    :return: View Prepaid (if aunthenticated) or Login Page (if not)
    """
    inactive_prepaid_cards = InactivePrepaid
    inactive_prepaid_cards.objects.using('external').filter(id=card_id).delete()
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        messages.success(request, 'Success! Inactive Prepaid Card id={} has been deleted.'.format(card_id))
        return redirect('/prepaid')
    else:
        return redirect('/')

def inactive_prepaid_activate(request, card_id):
    """ View for moving entry from Inactive Prepaid Card to AuthTable.
    :param request: HTTP Request
    :type request: object
    :param card_id: Inactive Prepaid Card ID
    :type card_id: str
    :return: View AuthTable (if aunthenticated) or Login Page (if not)
    """
    try:
        auth_table, packages, inactive_prepaid_cards = AuthTable, Packages, InactivePrepaid
        inactive_prepaid_card = inactive_prepaid_cards.objects.using('external').get(id=card_id)
        inactive_prepaid_card.id = None
        package = packages.objects.using('external').get(TypeID=inactive_prepaid_card.typeid)
        endofsubscription = datetime.datetime.now().replace(microsecond=0) + datedelta.datedelta(months=int(package.billperiod))
        auth_table.objects.using('external').create(userlogin=inactive_prepaid_card.userlogin, 
                                                    accounttype="prepaid", status=1, 
                                                    endofsubscription=endofsubscription)
        inactive_prepaid_cards.objects.using('external').filter(id=card_id).delete()
        messages.success(request, 'Inactive Prepaid Card id={}, userlogin={} has been activated.'.format(card_id, inactive_prepaid_card.userlogin))
        return redirect('/subscribers')
    except InactivePrepaid.DoesNotExist:
        messages.error(request, "Error! Unable to find Inactive Prepaid Card with choosen id {}".format(card_id))
        return redirect('/prepaid')
    except Packages.DoesNotExist:
        messages.error(request, 'Error! Unable to find TypeID of the Package that was assigned to choosen Inactive Prepaid Card!')
        return redirect('/prepaid')
    except IntegrityError:
        messages.error(request, "Error! Could not Activate Inactive Prepaid Card for userlogin='{}', entry already exists in the AuthTable.".format(inactive_prepaid_card.userlogin))
        return redirect('/prepaid')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/prepaid')