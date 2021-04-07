import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.db import IntegrityError

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import User, Post, Like


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
def like(request, post_id):
    likes = Like.objects.get(liker=request.user)

    post = Post.objects.get(id=post_id)

    likes.post.add(post)

    if request.method == "PUT":
        return HttpResponse("put")
        # data = json.loads(request.liked)
        # if data.get("liked") is not None:
            
            

    
    return HttpResponse(likes)
    
    # except Like.DoesNotExist:
        # return JsonResponse("error": "not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.liked)
        if data.get("liked") is not None:
            like.liked = data["liked"]
        like.save()
        return HttpResponse(status=204)

            # like.
            ##################### I stopped here.

    return HttpResponse("hello")



@csrf_exempt
def post_view(request):

    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    # return HttpResponse(posts)
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def compose(request):

    # check if post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # load the data
    data = json.loads(request.body)

    # Get the Post contents
    body = data.get("body", "")
    author = User.objects.get(id=request.user.id)

    # Save the post
    post = Post(author=author, body=body)
    post.save()

    return JsonResponse({
        "hello": "this worked"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
