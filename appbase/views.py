from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, get_user
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
User = get_user_model()
DEFAULT_REDIRECT_URL = "home"


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
                login(request, user)
                return redirect("home")

        else:
            messages.info(request, "please check passwords")  # TODO messages info alert difference bak
            return redirect("register")

    return render(request, "register.html")


def mylogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        next = request.POST.get("next", DEFAULT_REDIRECT_URL)
        if user:
            login(request, user)
            return redirect(next)
            # return redirect("home")
        else:
            messages = []
            messages.append("something is wrong")
            return render(request, "login.html", {"messages": messages, "next": next})
            # messages.info(request, "something is wrong")
            # return redirect("login")

    next = request.GET.get("next", DEFAULT_REDIRECT_URL)
    return render(request, "login.html", {"next": next})


def mylogout(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        picture = request.FILES.get("picture")

        user.profile.bio = bio
        user.profile.location = location
        if picture:  # Only update the picture if a new file is provided
            user.profile.picture = picture
        user.profile.save()
        return redirect("profile")

    return render(request, "profile.html", {"user": user})
