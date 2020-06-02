from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

#新規登録画面の作成
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )
            messages.success(request, username + 'さんのアカウントが作成されました')
            return redirect('login')

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

#ログインページの作成
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'ユーザー名、もしくはパスワードに誤りがあります')

    context = {

    }
    return render(request, 'accounts/login.html', context)

#ログアウト処理の作成
def logoutUser(request):
    logout(request)
    return redirect('login')

#ホーム画面の作成
@login_required(login_url='login')
@admin_only
def home(request):
    #注文全て
    orders = Order.objects.all()
    #顧客全て
    customers = Customer.objects.all()
    #顧客数
    total_customers = customers.count()
    #注文合計
    total_orders = orders.count()
    #配達済み
    delivered = orders.filter(status='Delivered').count()
    #保留中
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
	    'total_orders':total_orders,
        'total_customers':total_customers,
        'delivered':delivered,
	    'pending':pending
        }

    return render(request, 'accounts/dashbord.html', context)

#ユーザーページ
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    #注文全て
    orders = request.user.customer.order_set.all()
    #注文合計
    total_orders = orders.count()
    #配達済み
    delivered = orders.filter(status='Delivered').count()
    #保留中
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request, 'accounts/user.html', context)

#カスタマープロフィール画面の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form':form,
    }
    return render(request, 'accounts/account_settings.html', context)

#商品一覧画面の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

#顧客管理画面の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter,
    }
    return render(request, 'accounts/customer.html', context)

#注文追加処理の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status','note'), extra=6)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset':formset,
    }
    return render(request, 'accounts/order_form.html', context)

#注文編集処理の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form':form,
    }
    return render(request, 'accounts/update_order.html', context)

#注文削除処理の作成
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request
, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {
        'item':order
    }
    return render(request, 'accounts/delete.html', context)
    