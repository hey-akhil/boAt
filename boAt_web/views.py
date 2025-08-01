from django.shortcuts import render , redirect
from .forms import CustomUserCreationForm, ProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    contex = {}
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
            return redirect('home')  # Redirect to product listing or home
    else:
        form = ProductForm()
    return render(request, 'boAt/add_product.html', {'form': form})