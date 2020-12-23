# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Packages, PackagesForm
from django.contrib import messages
from django.db.models import Q
# For testing
from ..models import AuthTable, AuthTableForm


def packages_main(request):
    """ View for rendering entries of Packages.
    :param request: HTTP Request
    :type request: object
    :return: View Packages (if authenticated) or Login Page (if not)
    """
    column_names = Packages._meta.get_fields()
    packages = Packages.objects.using('external').all().values().order_by('TypeID')[:10]
    data = {
        "title": "Packages",
        "request": request,
        "column_names": column_names,
        "packages": packages
    }
    if request.user.is_authenticated:
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def packages_search(request):
    """ View for searching entries of Packages.
    :param request: HTTP Request
    :type request: object
    :return: View Packages (if authenticated) or Login Page (if not)
    """
    column_names = Packages._meta.get_fields()
    keyword = request.GET['q']
    queries = [Q(**{'%s__icontains' % column.name: keyword}) for column in column_names]
    qs = Q()
    for query in queries:
        qs = qs | query
    packages = Packages.objects.using('external').filter(qs).values().order_by('TypeID')[:10]
    data = {
        "title": "Packages",
        "request": request,
        "column_names": column_names,
        "packages": packages
    }
    if request.user.is_authenticated:
        messages.info(request, 'Search results for keyword: "{}"'.format(keyword))
        return render(request, 'home/home.html', data)
    else:
        return redirect('/')

def packages_add(request):
    """ View for rendering form for adding Packages.
    :param request: HTTP Request
    :type request: object
    :return: Add Package (if authenticated) or Login Page (if not)
    """
    try:
        if request.method == 'POST':
            form = PackagesForm(request.POST)
            if form.is_valid():
                Packages = form.save(commit=False)
                Packages.save(using='external')
                messages.success(request, 'Success! Package has been added.')
                return redirect('/packages')
        else:
            form = PackagesForm()
        data = {
            "title": "Add Package",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Add Package, given TypeID already exists in the table.")
        return redirect('/packages')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/packages')

def packages_edit(request, package_id):
    """ View for rendering form for editing details of
        existing Package.
    :param request: HTTP Request
    :type request: object
    :param request: Package ID
    :type package_id: str
    :return: Edit Package (if authenticated) or Login Page (if not)
    """
    try:
        packages = Packages
        package = packages.objects.using('external').get(TypeID=package_id)
        if request.method == 'POST':
            form = PackagesForm(request.POST, instance=package)
            if form.is_valid():
                packages = form.save(commit=False)
                packages.save(using='external')
                messages.success(request, 'Success! Package id={} has been edited.'.format(package_id))
                return redirect('/packages')
        else:
            form = PackagesForm(instance=package)
        data = {
            "title": "Edit Package",
            "request": request,
            "form": form
        }
        if request.user.is_authenticated:
            return render(request, 'home/home.html', data)
        else:
            return redirect('/')
    except IntegrityError:
        messages.error(request, "Error! Could not Edit Package, this TypeID already exists in the table.")
        return redirect('/packages')
    except Exception as e:
        messages.error(request, "Error! "+ str(type(e)) + " | " + str(e))
        return redirect('/packages')

def packages_delete(request, package_id):
    """ View for deleting existing Package.
    :param request: HTTP Request
    :type request: object
    :param request: Package ID
    :type package_id: str
    :return: View Packages (if authenticated) or Login Page (if not)
    """
    packages = Packages
    packages.objects.using('external').filter(TypeID=package_id).delete()
    data = {
        "request": request
    }
    if request.user.is_authenticated:
        messages.success(request, 'Success! Package id={} has been deleted.'.format(package_id))
        return redirect('/packages')
    else:
        return redirect('/')
