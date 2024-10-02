from django.http import JsonResponse
from django.shortcuts import render,redirect
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json


def home (request):
    products=Product.objects.filter(trending=1)
    return render(request,"shops/index.html",{"products":products})

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
           data=json.load(request)
           print(data['product_qty'])
           print(data['pid'])
           print(request.user.id)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect ("/login")
        return render(request,"shops/login.html")


def register (request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now..!")
            return redirect('/login')
    return render(request,"shops/register.html",{'form':form})

def collections (request):
    categories=Category.objects.filter(status=0)
    return render(request,"shops/collections.html",{"categories":categories})

def collectionsview(request,name):
    if(Category.objects.filter(name=name ,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"shops/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such category Found")
        return redirect('collections')
    
def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=0).exists():
        if Product.objects.filter(name=pname, status=0).exists():
            product = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shops/products/product_details.html", {"product": product})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')
