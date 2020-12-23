# from django.contrib.auth.decorators import login_required
import datetime, datedelta
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from ..models import NullSpeedUnusedCafeCards, NullSpeedUnusedCafeCardsForm, AuthTable, AuthTableForm, Packages


def nullspeed_unused_cafe_main(request):
    """ View for rendering entries of Null Speed Unused Cafe.
    :param request: HTTP Request
    :type request: object
    :return: View Null Speed Unused Cafe (if aunthenticated) or Login Page (if not)
    """
    column_names = NullSpeedUnusedCafeCards._meta.get_fields()
    nullspeed_unused_cafe_cards = NullSpeedUnusedCafeCards.objects.using('external').all().values().order_by('id')[:10]
    data = {
        "title": "Null Speed Unused Cafe Cards",
        "request": request,
        "column_names": column_names,
        "nullspeed_unused_cafe_cards": nullspeed_unused_cafe_cards
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def nullspeed_unused_cafe_search(request):
    """ View for searching entries of Null Speed Unused Cafe.
    :param request: HTTP Request
    :type request: object
    :return: View Null Speed Unused Cafe (if authenticated) or Login Page (if not)
    """
    column_names = NullSpeedUnusedCafeCards._meta.get_fields()
    keyword = request.GET['q']
    queries = [Q(**{'%s__icontains' % column.name: keyword}) for column in column_names]
    qs = Q()
    for query in queries:
        qs = qs | query
    nullspeed_unused_cafe_cards = NullSpeedUnusedCafeCards.objects.using('external').filter(qs).values().order_by('id')[:10]
    data = {
        "title": "Null Speed Unused Cafe Cards",
        "request": request,
        "column_names": column_names,
        "nullspeed_unused_cafe_cards": nullspeed_unused_cafe_cards
    }
    if request.user.is_authenticated:
        messages.info(request, 'Search results for keyword: "{}"'.format(keyword))
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def nullspeed_unused_cafe_add(request):
    """ View for rendering form for adding Null Speed Unused Cafe.
    :param request: HTTP Request
    :type request: object
    :return: Add Null Speed Unused Cafe (if aunthenticated) or Login Page (if not)
    """
    try:
        if request.method == 'POST':
            form = NullSpeedUnusedCafeCardsForm(request.POST)
            if form.is_valid():
                NullSpeedUnusedCafeCards = form.save(commit=False)
                NullSpeedUnusedCafeCards.save(using='external')
                messages.success(request, 'Success! NullSpeed Unused Cafe Card has been added.')
                return redirect('/nullspeed/unused-cafe/')
        else:
            form = NullSpeedUnusedCafeCardsForm()
        data = {
            "title": "Add Null Speed Unused Cafe Card",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Add NullSpeed Unused Cafe Card, given userlogin already exists in the table.")
        return redirect('/nullspeed/unused-cafe')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/nullspeed/unused-cafe')

def nullspeed_unused_cafe_edit(request, card_id):
    """ View for rendering form for editing details of
        existing Null Speed Unused Cafe.
    :param request: HTTP Request
    :type request: object
    :param card_id: Null Speed Unused Cafe Card ID
    :type card_id: str
    :return: Edit Null Speed Unused Cafe (if aunthenticated) or Login Page (if not)
    """
    try:
        nullspeed_unused_cafe_cards = NullSpeedUnusedCafeCards
        nullspeed_unused_cafe_card = nullspeed_unused_cafe_cards.objects.using('external').get(id=card_id)
        if request.method == 'POST':
            form = NullSpeedUnusedCafeCardsForm(request.POST, instance=nullspeed_unused_cafe_card)
            if form.is_valid():
                nullspeed_unused_cafe_cards = form.save(commit=False)
                nullspeed_unused_cafe_cards.save(using='external')
                messages.success(request, 'Success! NullSpeed Regular User id={} has been edited.'.format(card_id))
                return redirect('/nullspeed/unused-cafe/')
        else:
            form = NullSpeedUnusedCafeCardsForm(instance=nullspeed_unused_cafe_card)
        data = {
            "title": "Edit Null Speed Unused Cafe Card",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Edit NullSpeed Unused Cafe Card, this userlogin already exists in the table.")
        return redirect('/nullspeed/unused-cafe')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/nullspeed/unused-cafe')

def nullspeed_unused_cafe_delete(request, card_id):
    """ View for deleting existing Null Speed Unused Cafe.
    :param request: HTTP Request
    :type request: object
    :param card_id: Null Speed Unused Cafe Card ID
    :type card_id: str
    :return: View Null Speed Unused Cafe (if aunthenticated) or Login Page (if not)
    """
    nullspeed_unused_cafe_cards = NullSpeedUnusedCafeCards
    nullspeed_unused_cafe_cards.objects.using('external').filter(id=card_id).delete()
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        messages.success(request, 'Success! NullSpeed Unused Cafe Card id={} has been deleted.'.format(card_id))
        return redirect('/nullspeed/unused-cafe')
    else:
        return redirect('/')

def nullspeed_unused_cafe_activate(request, card_id):
    """ View for moving entry from Null Speed Unused Cafe to AuthTable.
    :param request: HTTP Request
    :type request: object
    :param card_id: Null Speed Unused Cafe Card ID
    :type card_id: str
    :return: View AuthTable (if aunthenticated) or Login Page (if not)
    """
    try:
        auth_table, packages, nullspeed_unused_cafe_cards = AuthTable, Packages, NullSpeedUnusedCafeCards
        nullspeed_unused_cafe_card = nullspeed_unused_cafe_cards.objects.using('external').get(id=card_id)
        nullspeed_unused_cafe_card.id = None
        package = packages.objects.using('external').get(TypeID=nullspeed_unused_cafe_card.typeid)
        endofsubscription = datetime.datetime.now().replace(microsecond=0) + datedelta.datedelta(months=int(package.billperiod))
        auth_table.objects.using('external').create(userlogin=nullspeed_unused_cafe_card.userlogin, 
                                                    accounttype="null-cafe", status=1, 
                                                    endofsubscription=endofsubscription)
        nullspeed_unused_cafe_cards.objects.using('external').filter(id=card_id).delete()
        messages.success(request, 'NullSpeed Unused Cafe Card id={}, userlogin={} has been activated.'.format(card_id, nullspeed_unused_cafe_card.userlogin))
        return redirect('/subscribers')
    except NullSpeedUnusedCafeCards.DoesNotExist:
        messages.error(request, "Error! Unable to find NullSpeed Unused Cafe Card with choosen id {}".format(card_id))
        return redirect('/nullspeed/unused-cafe')
    except Packages.DoesNotExist:
        messages.error(request, 'Error! Unable to find TypeID of the Package that was assigned to choosen NullSpeed Unused Cafe Card!')
        return redirect('/nullspeed/unused-cafe')
    except IntegrityError:
        messages.error(request, "Error! Could not Activate NullSpeed Unused Cafe Card for userlogin='{}', entry already exists in the AuthTable.".format(nullspeed_unused_cafe_card.userlogin))
        return redirect('/nullspeed/unused-cafe')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/nullspeed/unused-cafe')