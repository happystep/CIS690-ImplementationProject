from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import math
from .models import Item, Vendor, Order, Location, Category, StockControl

import pandas as pd

# Create your views here.


def home(request):
    stock = StockControl.objects.all()
    return render(request, 'inventory/home.html', {'query_results': stock})

@csrf_exempt
def item(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        cost_per_item = request.POST.get('cost');
        cur = request.POST.get('reorder')
        if cur == "False":
            discontinued = False
        else:
            discontinued = True
        name = request.POST.get('name')
        Item.objects.create(description=description, cost_per_item=cost_per_item, item_discontinued=discontinued, name=name )
        # return redirect(request, 'inventory/orders.html')
    item = Item.objects.all()
    return render(request, 'inventory/item.html', {'query_results': item})

@csrf_exempt
def vendor(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        Vendor.objects.create(description=description)
        # return redirect(request, 'inventory/orders.html')
    vendor = Vendor.objects.all()
    return render(request, 'inventory/vendor.html', {'query_results': vendor})

@csrf_exempt
def new_vendor(request):
    return render(request, 'inventory/new_vendor.html', {})

@csrf_exempt
def location(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        Location.objects.create(description=description)
        # return redirect(request, 'inventory/orders.html')
    location = Location.objects.all()
    return render(request, 'inventory/location.html', {'query_results': location})

@csrf_exempt
def new_location(request):
    return render(request, 'inventory/new_location.html', {})


@csrf_exempt
def category(request):
    if request.method == 'POST':
        category = request.POST.get('description')
        Category.objects.create(category=category)
        # return redirect(request, 'inventory/orders.html')
    category = Category.objects.all()
    return render(request, 'inventory/category.html', {'query_results': category})

@csrf_exempt
def new_category(request):
    return render(request, 'inventory/new_category.html', {})


@csrf_exempt
def orders(request):
    if request.method == 'POST':
        selected_vendor = request.POST.get('vendor')
        current_vendor = Vendor.objects.get(description=selected_vendor)
        selected_item = request.POST.get('item');
        current_item = Item.objects.get(name=selected_item)
        selected_reorder = request.POST.get('reorder')
        Order.objects.create(reorder=selected_reorder, item=current_item, vendor=current_vendor)
        # return redirect(request, 'inventory/orders.html')
    order = Order.objects.all()
    return render(request, 'inventory/orders.html', {'query_results': order})

@csrf_exempt
def new_order(request):
    items = Item.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'inventory/new_order.html', {'items': items, 'vendors': vendors})


@csrf_exempt
def new_item(request):
    return render(request, 'inventory/new_item.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')
    # Redirect to a success page.


def login(request):
    if request.POST:
        if 'login' in request.POST:
            return HttpResponseRedirect('/youloggedin/')
        else:
            return HttpResponseRedirect('/youregistered')
    else:
        return render(request, 'inventory/login.html')


def login(request):
    if request.POST:
        if 'login' in request.POST:
            return HttpResponseRedirect('/youloggedin/')
        else:
            return HttpResponseRedirect('/youregistered')
    else:
        return render(request, 'inventory/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})


def simple_upload(request):
    if request.method == 'POST':
        new_types = request.FILES['myfile']

        # django.setup()
        csv = pd.read_csv(request.FILES['myfile'])
        col_names = list(csv.columns.values)
        # the first column name will be for pokemon
        pokemon_model_att = ''
        model_att = ''
        # get the model variables based off of column names
        check_names = (col_names[0], col_names[1])

        column_1_name = col_names[0]
        column_2_name = col_names[1]

        column_1_dataframe = csv[[col_names[0]]]
        print(column_1_dataframe)
        column_2_dataframe = csv[[col_names[1]]]
        # print(poke_num)
        # print(type_num)
        already_checked = []

        if check_names == ('Item Name', 'Item Number'):
            column_3_dataframe = csv[[col_names[2]]]  # item description
            column_4_dataframe = csv[[col_names[3]]]  # cost per item
            column_5_dataframe = csv[[col_names[4]]]  # item discontinued
            for value in range(csv.shape[0]):
                col1_val = column_1_dataframe.at[value, col_names[0]]
                col2_val = column_2_dataframe.at[value, col_names[1]]  # NOT USED
                col3_val = column_3_dataframe.at[value, col_names[2]]
                col4_val = column_4_dataframe.at[value, col_names[3]]
                col5_val = column_5_dataframe.at[value, col_names[4]]
                if math.isnan(col5_val):
                    discontinued = False
                elif col5_val == 0:
                    discontinued = False
                else:
                    discontinued = True
                if math.isnan(col4_val):
                    col4_val = 0
                Item.objects.create(description=col3_val, cost_per_item=col4_val, item_discontinued=discontinued, name=col1_val)
                print('item added ' + str(col1_val) + ' ' + str(col3_val))
        elif check_names == ('vendor id', 'vendor description'):
            for value in range(csv.shape[0]):
                col1_val = column_1_dataframe.at[value, col_names[0]]
                col2_val = column_2_dataframe.at[value, col_names[1]]
                Vendor.objects.create(description=col2_val)
                print('Vendor Added ' + str(col1_val) + ' ' + str(col2_val))
        elif check_names == ('idOrder', 'reorder'):
            column_3_dataframe = csv[[col_names[2]]]  # item number
            column_4_dataframe = csv[[col_names[3]]]  # vendor number
            column_5_dataframe = csv[[col_names[4]]]  # date of last order
            for value in range(csv.shape[0]):
                col1_val = column_1_dataframe.at[value, col_names[0]]  # not used
                col2_val = column_2_dataframe.at[value, col_names[1]]
                col3_val = int(column_3_dataframe.at[value, col_names[2]])
                current_item = Item.objects.get(id=col3_val)
                col4_val = int(column_4_dataframe.at[value, col_names[3]])
                current_vendor = Vendor.objects.get(id=col4_val)
                col5_val = column_5_dataframe.at[value, col_names[4]]
                Order.objects.create(reorder= col2_val, item=current_item, vendor=current_vendor)
                print('Order added ' + ' ' + str(col2_val))
        elif check_names == ('IdLocations', 'Description'):
            for value in range(csv.shape[0]):
                col1_val = column_1_dataframe.at[value, col_names[0]]  # not used
                col2_val = column_2_dataframe.at[value, col_names[1]]  # description
                Location.objects.create(description=col2_val)
                print('Location added ' + ' ' + str(col2_val))
        elif check_names == ('CATEGORIES', 'IDCategories'):
            for value in range(csv.shape[0]):
                col1_val = column_1_dataframe.at[value, col_names[0]]  # category
                col2_val = column_2_dataframe.at[value, col_names[1]]  # not used
                Category.objects.create(category=col1_val)
                print('Category added ' + ' ' + str(col1_val))
        else:
            # 1 is idstockcontrol not used
            # 2 is item_number
            column_3_dataframe = csv[[col_names[2]]]  # category number
            column_4_dataframe = csv[[col_names[3]]]  # stock location number
            column_5_dataframe = csv[[col_names[4]]]  # stock quantity
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value, col_names[0]])  # NOT USED
                col2_val = int(column_2_dataframe.at[value, col_names[1]])
                current_item = Item.objects.get(id=col2_val)
                col3_val = int(column_3_dataframe.at[value, col_names[2]])
                current_category = Category.objects.get(id=col3_val)
                col4_val = int(column_4_dataframe.at[value, col_names[3]])
                current_location = Location.objects.get(id=col4_val)
                col5_val = column_5_dataframe.at[value, col_names[4]]
                StockControl.objects.create(item_number=current_item, stock_location=current_location, stock_quantity=col5_val, stock_category=current_category)
                print('stockcontrol added' + ' ' + str(col2_val))
    return render(request, 'inventory/simple_upload.html', {})
