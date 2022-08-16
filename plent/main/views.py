from tracemalloc import start
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from . import models

# Create your views here.

def checkAuthentication(f):
    def wrapper(request):
        if not request.user.is_authenticated:
            return render(request, "plent/login.html")
            
        return f(request)
    return wrapper 

@checkAuthentication
def index(request):
    return render(request, "plent/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return render(request, "plent/login.html", {
                "message": "username or password incorrect"
            })
        
        login(request, user)
        
        return render(request, "plent/index.html", {
            "username": username
        })
    else:
        return render(request, "plent/login.html")
    
@checkAuthentication
def logout_view(request):
    logout(request)
    return render(request, "plent/logout.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try: 
            user = User.objects.create_user(username=username, email="", password=password)
            user.save()
        except:
            return render(request, "plent/register.html", {
                "message": f"{username} already exists"
            })
        
        login(request, user)
        
        return render(request, "plent/index.html", {
            "username": username
        })
    else:
        return render(request, "plent/register.html")
    
@checkAuthentication
def addPost(request):
    if request.method == "POST":
        topic = request.POST["topic"]
        content = request.POST["content"]
    
        try:
            client = models.Client.objects.get(user=request.user)
        except ObjectDoesNotExist:
            client = models.Client(user=request.user)
            client.save()
        
        post = models.Post(topic=topic, content=content)
        post.save()
        
        post.authors.add(client)
            
        return render(request, "plent/addPost.html", {
                "message": "added"
            })
    else:
        return render(request, "plent/addPost.html")
    
@checkAuthentication
def posts(request):
    start = int(request.GET["start"]) -1
    end = int(request.GET["end"]) -1
    
    posts = models.Post.objects.order_by("-id")[start:end]
    
    data = serializers.serialize("json", posts)
    return HttpResponse(data)
    