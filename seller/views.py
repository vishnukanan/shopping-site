from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from .forms import SellerRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.contrib.auth.models import User
from .urls import *
from .urls import *
from .models import *
from django.contrib.auth.models import User


def register_seller(request):
    return render(request, 'seller.html', {'form': SellerRegistrationForm()})

def seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():  # Added parentheses to is_valid()
            password = form.cleaned_data.get('password')
            cpassword = form.cleaned_data.get('cpassword')
            if password != cpassword:
                messages.error(request, 'Passwords do not match')
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful. You can now login.')
                return HttpResponse('Registration successful. You can login now.')
    else:
        form = SellerRegistrationForm()
                
    return render(request, 'register_seller.html', {'form': form})


def enterview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f'You are logged in {username}')
                request.session['sellerid'] = user.id
                return redirect(productdisplay)
                
            else:
                messages.error(request, 'Invalid username or password')

                
        else:
            messages.error(request, 'Form is invalid')
    else:
        form = AuthenticationForm()

    return render(request, 'seller_log.html', {'form': form})

def seller_index(request):

    return render(request,'sellerindex.html')
def productdisplay(request):
    id1=request.session['sellerid']
    db=User.objects.get(id=id1)
    data=Sellproduct.objects.all()
    return render(request,'seller_product_display.html',{'db':db,'data':data})

def seldelete(request,id):
    data = Sellproduct.objects.get(id=id)
    data.delete()

    return render(request,'seldel.html')
def selupdate(request, id):
    data = get_object_or_404(Sellproduct, id=id)
    if request.method == 'POST':
        data.prodname = request.POST.get('name')
        data.prodprice = request.POST.get('price')
        data.prosize = request.POST.get('size')
        data.desc = request.POST.get('desc')
        data.category = request.POST.get('category') 

        if request.FILES.get('proimg') is not None:
            data.proimg = request.FILES.get('proimg')
        
        data.save()
        messages.success(request, 'Product updated successfully.')
        return redirect(productdisplay)
    

    return render(request, 'selupdate.html', {'data': data})








