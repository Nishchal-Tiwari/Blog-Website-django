from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import blog
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
import json

# request.POST only  parse ( multipart/form-data , application/x-www-form-urlencoded)
# so to parse json data we need to use json.loads(request.body)  and import json


def parse_data(request):
        content_type = request.META.get('CONTENT_TYPE', '')
        if 'application/json' in content_type:
            data=json.loads(request.body)
            return data
        elif 'multipart/form-data' in content_type:
            data=request.POST
            return data
        elif 'application/x-www-form-urlencoded' in content_type:
            data=request.POST
            return data
        else:
            return HttpResponse("Unknown type of data")
            print("Unknown type of data")
        
# Authentication APIs

def login_user(request):
    if request.method == 'POST':
        data=parse_data(request)
        if(data.get('username') is None or data.get('password') is None):
            return render(request,'signin.html',{'msg':"Invalid request , username or password is missing"}) 
        
        username = data['username']
        password = data['password']
        if username is '' or password is '':
            return render(request,'signin.html',{'msg':"No fields can be empty"})
        user = authenticate(username=username, password=password)
        print(user,' ','user')
        if user is not None:
             login(request, user)
             return redirect('/')
        return render(request,'signin.html',{'msg':'Invalid Credentials'})
        # return HttpResponse({'status':401, 'message':'Invalid Credentials'},content_type='application/json')
    else:
        if(  request.user.is_authenticated):
            return redirect('/')
        return render(request,'signin.html')
        

def logout_user(request):
    logout(request)
    return redirect('/signin/')


def register_user(request):
    if request.method == 'POST':
        data=parse_data(request)
        if(data.get('username') is None or data.get('password') is None):
            return render(request,'signup.html',{'msg':"Invalid request , username or password is missing"})
        username = data['username']
        password = data['password']
        if username is '' or password is '':
            return render(request,'signin.html',{'msg':"No fields can be empty"})
        
        ifuser=User.objects.filter(username=username).exists()
        print(ifuser,' ','ifuser')
        if ifuser is True:
            print("User already exists")
            return render(request,'signup.html',{'msg':'User already exists'})
        user=User.objects.create(username=username)
        user.set_password(password)
        # user.first_name = first_name
        # user.last_name = last_name
        # user.email = email
        user.save()
        return redirect('/signin/')
    else:
        return render(request,'signup.html')
def isAuth(request):
    if request.user.is_authenticated:
        return HttpResponse("User is authenticated")
    else:
        return HttpResponse("User is not authenticated") 
# Blog APIs

def addBlog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data=parse_data(request)
            print(request.FILES)
            if(data.get('title') is None or data.get('description') is None or data.get('slug') is None):
                return HttpResponse("Invalid request , title or description or slug is missing")
            title = data['title']
            description = data['description']
            slug=data['slug']
            image=''
            if 'image' in request.FILES:
                image = request.FILES['image']
            try:
                blog.objects.create(title=title,description=description,image=image,author=request.user,slug=slug)
            except:
                return render(request,'addblog.html',{'msg':"Blog with same slug already exists"})
            return redirect('/')
        
        else:
            return render(request,'addblog.html')
    else: 
        return render(request,'signin.html',{'msg':"User is not authenticated"}) 

def updateBlog(request,blogname):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data= parse_data(request)
            print(data.get('blogslug'),'sadfiuas f')
            if(data.get('blogslug') is None):
                return HttpResponse("Invalid request , slug is missing")
            try:
                prevblog=blog.objects.get(slug=data.get('blogslug'))
            except blog.DoesNotExist:
                return HttpResponse("Blog does not exist 2")
            if(request.user != prevblog.author):
                return HttpResponse("User is not authenticated")
            if(data.get('title')):
                prevblog.title=data.get('title')
            if(data.get('description')):
                prevblog.description=data.get('description')
            if(data.get('image')):
                prevblog.image=data.get('image')
            prevblog.save()
            return redirect('/')
        else:
            try:
                sblog=blog.objects.get(slug=blogname)
            except blog.DoesNotExist:
                return HttpResponse("Blog does not exist 1")
            return render(request,'updateblog.html',{'blog':sblog})
    else:
        return render(request,'signin.html',{'msg':"User is not authenticated"}) 
        
   
def deleteBlog(request,blogslug):
    if request.user.is_authenticated:
    
   
        try:
            blog.objects.get(slug=blogslug)
        except blog.DoesNotExist:
            return HttpResponse("Blog does not exist")
        prevblog=blog.objects.get(slug=blogslug)
        if(request.user != prevblog.author):
            return render(request,'signin.html',{'msg':"User is not authenticated"}) 
        blog.objects.filter(slug=blogslug).delete()
        return redirect('/')
    else:
        return render(request,'signin.html',{'msg':"User is not authenticated"}) 
            

def account(request):
    if(request.user.is_authenticated):
        blogs=blog.objects.filter(author=request.user)
        return render(request,'admin.html',{'blogs':blogs})
    else:
        return render(request,'signin.html',{'msg':"User is not authenticated"}) 

def home(request):
    blogs=blog.objects.all()

    return render(request,'blog.html',{'blogs':blogs})
def blogdetail(request,blogname):
    try:
        blogs=blog.objects.get(slug=blogname)
        return render(request,'blog_detail.html',{'blog':blogs})
    except blog.DoesNotExist:
        return redirect('/')
         
def data(request):
    if(request.method=='POST'):
        print(request.POST['name'])
    else :
        print("Data not found")
    return HttpResponse({'data':'data'},content_type='application/json')

    