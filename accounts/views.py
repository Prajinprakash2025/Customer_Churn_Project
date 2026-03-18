from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required   
                            
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "user/register.html")

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # block admin users from customer login
            if user.is_staff or user.is_superuser:
                messages.error(request, "Admins must login through admin panel.")
                return redirect("login")

            login(request, user)
            return redirect("product_list")

        messages.error(request, "Invalid credentials")
        return redirect("login")

    return render(request, "user/login.html")
def user_logout(request):
    logout(request)
    return redirect("login")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("/management/")

        messages.error(request, "Invalid admin credentials")

    return render(request, "admin/admin_login.html")


@login_required
def profile(request):

    # block admin users
    if request.user.is_staff or request.user.is_superuser:
        return redirect("product_list")   # or admin dashboard

    return render(request, "user/profile.html")