from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, get_user
from .models import Profile, Post
from django.contrib.auth.decorators import login_required

# Create your views here.
User = get_user_model()
DEFAULT_REDIRECT_URL = "home"


def home(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        followed_users = profile.following.all()
        posts = Post.objects.filter(user__profile__in=followed_users).order_by("-created_at")

        # Suggest users that the authenticated user is NOT following
        suggested_users = (
            Profile.objects.exclude(id__in=followed_users.values_list("id", flat=True))
            .exclude(user=request.user)  # Exclude the authenticated user
            .order_by("?")[:5]
        )  # Limit to 5 suggestions

        return render(request, "home.html", {"posts": posts, "suggested_users": suggested_users})
    else:
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
                # Profile.objects.create(user=user) created at modelspy via signals
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


def createpost(request):
    user = request.user
    if request.method == "POST":
        caption = request.POST.get("caption")
        image = request.FILES.get("image")
        if image:
            Post.objects.create(caption=caption, user=user, image=image)
            return redirect("home")
    return render(request, "createpost.html")


def postdetail(request):
    return render(request, "postdetail.html")


def myposts(request):
    return render(request, "myposts.html")


def user(request, username):
    visiteduser = User.objects.get(username=username)
    is_following = False  # Default value
    if request.user.is_authenticated:
        is_following = request.user.profile.following.filter(id=visiteduser.profile.id).exists()
    if request.method == "POST":
        user = request.user
        action = request.POST.get("action")
        if action == "follow":
            user.profile.following.add(visiteduser.profile)
            visiteduser.profile.followers.add(user.profile)
        elif action == "unfollow":
            user.profile.following.remove(visiteduser.profile)
            visiteduser.profile.followers.remove(user.profile)
        # Recalculate `is_following` after the action
        is_following = request.user.profile.following.filter(id=visiteduser.profile.id).exists()

    return render(request, "user.html", {"visiteduser": visiteduser, "is_following": is_following})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)  # Unlike the post
    else:
        post.likes.add(user)  # Like the post

    # Redirect back to the referring page or a default URL
    return redirect(request.META.get("HTTP_REFERER", "/"))
