from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile

# Create your views here.
User = get_user_model()


def home(request):
    return render(request, "home.html")


def myregister(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")  # TODO bu alan djangonun kullandigimi gercekten ?
        password2 = request.POST.get("password2")

        if password1 and password2 and password1 == password2:  # TODO manuel olani ve auto olani yap
            isuseralready = User.objects.filter(username=username).exists()
            if isuseralready:
                messages.info(request, "the username is already taken")
                return redirect("register")
            else:
                # TODO burda hata olursa nasil bildirir templatede ne gerekli
                user = User.objects.create_user(username=username, password=password1)
                Profile.objects.create(user=user)

                return redirect("home")

        else:
            messages.info(request, "please check passwords")  # TODO messages info alert difference bak
            return redirect("register")

    return render(request, "register.html")


def mylogin(request):
    pass


def mylogout(request):
    pass
