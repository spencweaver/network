import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator


from .models import User, Post, Like, UserUser


# Redirect to the index path
def home(request):
    return HttpResponseRedirect(reverse("index", args=[0]))


def index(request, user_id):
    # initialize following and user_profile
    following = True

    # Check to see if following view
    view = request.GET.get('view', 0)
    if view != 0:
        user_profile = 'Following Posts'
        # Get the follower
        try:
            follower = UserUser.objects.get(follower=view)
            following = follower.following.all()

            # Create empty object of posts
            posts = Post.objects.none()

            # query for all the posts and merge
            for f in following:
                post = Post.objects.filter(author=f.id)
                posts = post | posts
        except ObjectDoesNotExist:
            return render(request, "network/error.html", {
                "error": "You are not following anyone"
            })

    # Make sure it is not the index path
    elif user_id > 0:
        user_profile = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user_profile)
        f = request.user.followers.all()
        # return HttpResponse(f)
        if not request.user.followers.filter(following=user_profile.id).exists():
            following = False
                
    else: 
        user_profile = None
        posts = Post.objects.all()

    # Order the posts and paginate
    posts = posts.order_by("-timestamp").all()
    page_number = request.GET.get('page', 1)
    p = Paginator(posts, 10)
    return render(request, "network/index.html", {
        "user_profile": user_profile,
        "page": p.page(page_number),
        "user_profile": user_profile,
        "following": following,
        "like": like,
    })


@csrf_exempt
def edit(request, post_id):
    # Make sure the post exists
    try:
        post = Post.objects.get(id=post_id)
    except Post.doesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == 'POST':
        # load the data
        data = json.loads(request.body)

        # get the edit content and update
        body = data.get("body_edit", "")
        post.body = body
        post.save()

        # give to fetch function
    return JsonResponse(post.serialize())


@csrf_exempt
def follow(request, user_id):
    # Get the object to follow
    following = User.objects.get(id=user_id)
    
    # Check if the following object exists
    try:
        useruser = UserUser.objects.get(follower=request.user)
    except ObjectDoesNotExist:
        useruser = None
    
    # check if already following
    if request.user.followers.filter(following=following).exists():
        useruser.following.remove(following)
        
    # Create object if does not exist
    elif useruser is None:
        useruser = UserUser(follower=request.user)
        useruser.save()
        useruser.following.add(following)
    
    # add the user to following list
    else:
        useruser.following.add(following)

    return HttpResponseRedirect(reverse("index", args=[user_id]))


@csrf_exempt
def like(request, post_id):
    # get the put information
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") is not None:
            archive = data["liked"]
    # Look up the post
    post = Post.objects.get(id=post_id)
    
    # if object exists
    try:
        likes = Like.objects.get(liker=request.user)
    except ObjectDoesNotExist:
        likes = None

    # Create a new likes list
    if likes is None:
        likes = Like(liker=request.user)
        likes.save()

    # Check to see if already liked
    elif request.user.likers.filter(post=post).exists():
        likes.post.remove(post)
    
    # add like to post
    else:
        likes.post.add(post)
    
    # Save the change
    post.save()      
    return JsonResponse(post.serialize())    


@csrf_exempt
def post_view(request):

    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    p = Paginator(posts, 10)
    p.count
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
            return HttpResponseRedirect(reverse("index", args=[0]))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", args=[0]))


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
        return HttpResponseRedirect(reverse("index", args=[0]))
    else:
        return render(request, "network/register.html")
