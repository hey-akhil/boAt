from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User



def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_user.html', {'users': users})



# Edit user
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('manage_users')
    return render(request, 'edit_user.html', {'user': user})

# Delete user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')


def home(request):
    data = AddProduct.objects.all()
    contex = {'data' : data}
    return render(request, 'boAt/home.html', contex)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')

    contex = {}
    return render(request, 'boAt/login.html', contex)

def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created successfully')
            return redirect('login')
    contex = {'form' : form}
    return render(request, 'boAt/register.html', contex)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'boAt/profile.html', {'user': request.user})



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data stored in Database')
            return redirect('add_product')
        else:
            messages.error(request, 'Something went wrong. Please check the form.')
    else:
        form = ProductForm()
    return render(request, 'boAt/add_product.html', {'form': form})




def viewProduct(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = AddProduct.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(badge__icontains=query) |
            Q(playback_badge__icontains=query)
        )

    if category:
        category_map = {
            'earbuds': 'Earbuds',
            'smartwatches': 'Smartwatch',
            'speakers': 'Speaker',
            'neckbands': 'Neckband',
        }
        cat_value = category_map.get(category.lower())
        if cat_value:
            products = products.filter(title__icontains=cat_value)

    context = {
        'product_data': products,
        'filtered_count': products.count(),
        'active_category': category
    }
    return render(request, 'boAt/viewProduct.html', context)


def product_detail(request, id):
    product = AddProduct.objects.get(id=id)
    return render(request, 'boAt/product_detail.html', {'product': product})


def manage_products(request):
    products = AddProduct.objects.all()
    return render(request, 'boAt/manage_products.html', {'products': products})

def edit_product(request, pk):
    product = get_object_or_404(AddProduct, id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated successfully!')
            return redirect('manage_products')  # Redirect after success
    else:
        form = ProductForm(instance=product)

    return render(request, 'boAt/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    product = get_object_or_404(AddProduct, pk=pk)
    product.delete()
    return redirect('manage_products')


def GiftStore(request):
    contex = {}
    return render(request, 'boAt/gift_store.html', contex)

def manage_user(request):
    contex = {}
    return render(request, 'boAt/manage_user.html', contex)

def saleLive(request):
    data = AddProduct.objects.all()
    contex = {'data': data}
    return render(request, 'boAt/sale_is_live.html', contex)


