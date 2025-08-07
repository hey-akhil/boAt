from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required





@staff_member_required
def admin_orders_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'boAt/admin_manage_orders.html', {'orders': orders})

def update_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to '{new_status.title()}'.")
        else:
            messages.error(request, "Invalid status selected.")
    return redirect('admin_orders')

# @staff_member_required
# def admin_order_detail_view(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         if new_status in dict(Order.STATUS_CHOICES):
#             order.status = new_status
#             order.save()
#             return redirect('admin_order_detail', order_id=order_id)
#
#     return render(request, 'admin_order_detail.html', {'order': order})
#

# -----------------------------------User Side----------------------------------------
#Regustartions
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

#Login Page
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

#User-HomePage
def home(request):
    data = AddProduct.objects.all()
    contex = {'data' : data}
    return render(request, 'boAt/home.html', contex)


def GiftStore(request):
    contex = {}
    return render(request, 'boAt/gift_store.html', contex)

def saleLive(request):
    data = AddProduct.objects.all()
    contex = {'data': data}
    return render(request, 'boAt/sale_is_live.html', contex)

#Logout User
def logoutUser(request):
    logout(request)
    return redirect('login')



# ------------------------------------Manage user-------------------------------------
@login_required
def profile_view(request):
    return render(request, 'boAt/profile.html', {'user': request.user})

def manage_user(request):
    form = User.objects.all()
    contex = {'form': form}
    return render(request, 'boAt/manage_user.html', contex)

#Add user
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            request.session['user_added'] = True
            return redirect('manage_user')
    else:
        form = CustomUserCreationForm()
    user_added = request.session.pop('user_added', False)
    return render(request, 'boAt/add_user.html', {'form': form, 'user_added': user_added})

# Edit user
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('manage_user')
    return render(request, 'boAt/edit_user.html', {'user': user})

# Delete user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_user')

# ---------------------------------Manage Products -----------------------------------

#Add Products
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

#view Product
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

#product_detail
def product_detail(request, id):
    product = AddProduct.objects.get(id=id)
    return render(request, 'boAt/product_detail.html', {'product': product})

#manage_products
def manage_products(request):
    products = AddProduct.objects.all()
    return render(request, 'boAt/manage_products.html', {'products': products})

#edit_product
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

#delete_product
def delete_product(request, pk):
    product = get_object_or_404(AddProduct, pk=pk)
    product.delete()
    return redirect('manage_products')


# ---------------------------------Manage User Carts  -----------------------------------

@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart_items = []

    # Backend calculations
    subtotal = sum(item.quantity * item.product.price for item in cart_items)
    tax = round(subtotal * 0.18, 2)
    shipping = 50 if subtotal < 1000 else 0
    total = round(subtotal + tax + shipping, 2)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'boAt/cart.html', context)


#Add to Cart
def add_to_cart(request, product_id):
    product = get_object_or_404(AddProduct, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()

    subtotal = sum(i.total_price() for i in CartItem.objects.filter(cart__user=request.user))
    tax = round(subtotal * 0.18, 2)
    shipping = 50 if subtotal < 1000 else 0
    total = subtotal + tax + shipping

    return JsonResponse({
        'quantity': item.quantity,
        'item_total': item.total_price(),
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    })

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    removed = False
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
        removed = True

    subtotal = sum(i.total_price() for i in CartItem.objects.filter(cart__user=request.user))
    tax = round(subtotal * 0.18, 2)
    shipping = 50 if subtotal < 1000 else 0
    total = subtotal + tax + shipping

    return JsonResponse({
        'removed': removed,
        'item_id': item_id,
        'quantity': item.quantity if not removed else 0,
        'item_total': item.total_price() if not removed else 0,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
        'removed_item_id': item_id if removed else None,
    })

@login_required
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')  # Adjust to your cart URL name

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        cart_items = cart.items.all()
        subtotal = sum(item.total_price() for item in cart_items)
        tax = subtotal * Decimal('0.18')
        shipping = Decimal('50.00')  # Flat rate shipping
        total = subtotal + tax + shipping

        order = Order.objects.create(
            user=request.user,
            first_name=full_name,
            address=address,
            phone=phone,
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart.items.all().delete()

        messages.success(request, "Your order has been placed successfully.")
        return redirect('order_success')  # You can make this URL

    else:
        cart_items = cart.items.all()
        subtotal = sum(item.total_price() for item in cart_items)
        tax = subtotal * Decimal('0.18')
        shipping = Decimal('50.00')
        total = subtotal + tax + shipping

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
        return render(request, 'boAt/checkout.html', context)


def order_success(request):
    return render(request, 'boAt/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'boAt/my_orders.html', {'orders': orders})
















# ---------------------------------------------------------------------------------
# --------------------------------- Admin Dashboard -------------------------------
# ---------------------------------------------------------------------------------

def admin_dashboard(request):
    users = User.objects.all()
    products = AddProduct.objects.all()
    orders = Order.objects.all()
    context = {'users' : users, 'products':products, 'orders' : orders}
    return render(request, 'boAt/admin_dashboard.html', context)

#Users list admin
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'boAt/view_user.html', {'user': user})






