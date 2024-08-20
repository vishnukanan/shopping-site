from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.models import User
from app.forms import LoginForm
from django.conf import settings 
from django.core.mail import send_mail
import stripe
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        propic = request.FILES.get('pic')
        mobile = request.POST.get('mobile')
        gender= request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            data = userregister(fullname=fullname, email=email, phone=mobile, gender=gender, propic=propic, password=password)
            data.save()
        else:
            return HttpResponse('Registration failed')
    return render(request, 'register.html')

def view_login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            data = userregister.objects.all()
            for i in data:
                if i.email == email and i.password == password:
                    request.session['userid'] = i.id
                    return redirect(userprofile)  # Assuming 'userprofile' is the name of the URL pattern
            return HttpResponse('login failed')
        else:
            return render(request, 'login.html')
    except KeyError:
        return redirect(view_login)

def userprofile(request):
    id1=request.session['userid']
    data=userregister.objects.get(id=id1)
    db=Sellproduct.objects.all()
    category=request.GET.get('category','all')
    #selected category will work if there is no category
    if category =='all':
        db=Sellproduct.objects.all()
    else:
        db=Sellproduct.objects.filter(category=category)
    for item in db:
        item.prosize=item.prosize.split(',')

    return render(request,'userprofile.html',{'data':data,'db':db})
def viewdet(request,id):
    data=userregister.objects.get(id=id)
    return render(request,'viewdeatils.html',{'data':data})
def updatepro(request):
    id1 = request.session['userid']
    data=userregister.objects.get(id=id1)
    if request.method=='POST':
        data.fullname=request.POST.get('fullname')
        data.email=request.POST.get('email')
        if request.FILES.get('img')==None:
            data.save()
        else:
            data.propic=request.FILES.get('img')
        data.gender=request.POST.get('gender')
        data.save()
        return redirect(userprofile)
    return render(request,'update.html',{'data':data})

def product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('img')  # Use FILES to get the uploaded image
        price = request.POST.get('price')
        size = request.POST.get('size')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        db=Sellproduct(prodname=name,prodprice=price,proimg=image,prosize=size,desc=desc,category=category)
        db.save()
        return HttpResponse('success')

    return render(request,'product.html')

def addtocart(request,id):
    
    item=Sellproduct.objects.get(id=id)
    size=''
    if request.method=='GET':
        size=request.GET.get('size')
        
        cart=Cart.objects.all()
        for i in cart:
            if i.item.id == id and i.selected_size==size and i.userid==request.session['userid']:
                i.quantity+=1
                i.save()
                return HttpResponse('item already in cart incremented')
            


        else:
            userid = request.session['userid']
            db=Cart(userid = userid,item=item,selected_size=size)
            db.save()
            return  HttpResponse('new item added to cart')
    return render(request,'cart.html',{'db':db})

def cartdisplay(request):
    
    userid=request.session['userid']

    db=Cart(userid=userid)
    db=Cart.objects.filter(userid=userid)

    tot=0
    count=0
    for i in db:
        i.total=i.item.prodprice*i.quantity
        tot+=i.total
        count+=1
        
    return render(request,'cartdis.html',{'db':db,'total_price':tot,'vis':userid,'count':count})
def inc_increment(request,itemid):
    db=Cart.objects.get(id=itemid)
    action=request.GET.get('action')
    if action=='increment':
        db.quantity+=1
        db.save()
    elif action=='decrement' and db.quantity>1:
        db.quantity-=1
        db.save()
    return redirect(cartdisplay)

def delete(request,id):
    db=Cart.objects.get(id=id)
    db.delete()
    return redirect(cartdisplay)
def addtowish(request,id):
    item=Sellproduct.objects.get(id=id)
    wish=Wishpage.objects.all()
    userid=request.session['userid']
    size=''
    if request.method=='GET':
        size=request.GET.get('size')
    
    
    for i in wish:
        
        if (i.item.id==id and i.userid==userid):

            # c=[]
            # if i in c:
            i.save()
            return redirect(userprofile)
            
        

            
    else:
        userid = request.session['userid']
        db=Wishpage(userid=userid,item=item)
        db.save()
        return redirect(userprofile)
        
    # return render(request,'wish.html',{'db':db})
   
    
def wishdisplay(request):
    item=Sellproduct.objects.all()
    
    userid=request.session['userid']
    db=Wishpage(userid=userid)
    db=Wishpage.objects.filter(userid=userid)
    for i in db:
        i.item.prosize=i.item.prosize.split(',')
     
    return render(request,'wishdisplay.html',{'db':db,'vist':userid})

def deletewish(request,id):
    
    db=Wishpage.objects.get(id=id)
    db.delete()
    return redirect(wishdisplay)

# def request(request,id):
#     db=
#     return render(request,'wishtocart.html')


def Adress(request):
    id1=request.session['userid']
    userdata=userregister.objects.get(id=id1)
    if request.method=='POST':
        contact_name=request.POST.get('contact_name')
        contact_num=request.POST.get('contact_num')
        adress1=request.POST.get('adress1')
        adress2=request.POST.get('adress2')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        db=Adressdet(userdetails=userdata,adress1=adress1,adress2=adress2,pincode=pincode,city=city,state=state,contact_name=contact_name,contact_num=contact_num)
        db.save()
        return redirect(deliverydet)
    else:

        return render(request,'adress.html')
def deliverydet(request):
    userid=request.session['userid']
    data=Adressdet.objects.filter(userdetails__id=userid)

    return render(request,'addview.html',{'data':data})


def summarypage(request):
    userid=request.session['userid']
    adress_id=request.GET.get('adr')
    print(adress_id)
    adress=Adressdet.objects.get(id=adress_id)
    cartitems=Cart.objects.filter(userid=userid)
    key=settings.STRIPE_PUBLISHABLE_KEY
    total=0
    striptotal=0
    for i in cartitems:
        total+=i.item.prodprice
        striptotal=total*100 # striptotal * 100 give original price
    return render(request,'summary.html',{'adress':adress,'cartitems':cartitems,'total':total,'striptotal':striptotal,'key':key})
def charges(request):
    return render(request,'charge.html')

def createorder(request):
    if request.method=='POST':
        order_items=[]
        total_price=0
        userid=request.session['userid']
        user=userregister.objects.get(id=userid)
        adress_id=request.POST.get('adress_id')
        adress=Adressdet.objects.get(id=adress_id)
        cart=Cart.objects.filter(userid=userid)
        order=Order.objects.create(userdetails=user,adress=adress)



        for i in cart:
            OrderItem.objects.create(
                order=order,
                order_pic=i.item.proimg,
                pro_name=i.item.prodname,
                quantity=i.quantity,
                price=i.item.prodprice
                

            )
            total_price+=i.item.prodprice*i.quantity
            order_items.append({
                'product':i.item.prodname,
                'quantity':i.quantity,
                'price':i.item.prodprice*i.quantity

            })
        expected_delivery_date=datetime.now()+timedelta(days=7)
        subject='order confirmation'
        context={
            'order_items':order_items,
            'total_price':total_price,
            'expected_delivery_date':expected_delivery_date.strftime('%Y-%m-%D')

        }
        html_message=render_to_string('order_confirmation_email.html',context)
        plain_message=strip_tags(html_message)    
        from_email='nkv92072@gmail.com'
        to_email=[user.email]

        send_mail(subject,plain_message,from_email,to_email,order_items)

        cart.delete()
        return HttpResponse('order created successfully')
    else:
        return HttpResponse('invalid request method')
    
    return render(request,'order.html')

def orderview(request):
    userid=request.session['userid']
    
    order=OrderItem.objects.filter(order__userdetails__id=userid).order_by('order__ordered_date')
    return render(request,'orderview.html',{'order':order})

def ordercancel(request,id):
    userid=request.session['userid']
    user=userregister.objects.get(id=userid)
    
    
    order=OrderItem.objects.get(id=id)
    order.status=False
    order.save()
    
    subject='order cancelled'


    context={
        'data':order
    }
    html_message=render_to_string('ordercancel.html',context)
    plain_message=strip_tags(html_message)    
    from_email='nkv92072@gmail.com'
    to_email=[user.email]
    send_mail(subject,plain_message,from_email,to_email)
    return HttpResponse('item cancelled')

def change_user_password(request):
    id1=request.session['userid']
    data=userregister.objects.get(id=id1)
    if request.method=='POST':
        oldpass=request.POST.get('password')
        new_password=request.POST.get('newpassword')
        cpass=request.POST.get('cpassword')
        if oldpass==data.password:
            if new_password==cpass:
                data.password=new_password
                data.save()
                return redirect(view_login)
            else:
                messages.error('please enter valid password')
        else:
            messages.error('please enter old password')
        
    subject='forgot password'
    html_message=render_to_string('forgotpass.html',{})
    plain_message=strip_tags(html_message)    
    from_email='nkv92072@gmail.com'
    to_email=[data.email]
    send_mail(subject,plain_message,from_email,to_email)


    return render(request,'change_pass.html',{'data':data,'visit':id1})

def logout(request):
    request.session.flush()
    return redirect(index)

def forgotpass(request):

    return render(request,'forgotpass.html',)



    



    

















    





        