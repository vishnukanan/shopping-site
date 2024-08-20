from django.db import models


# Create your models here.
class userregister(models.Model):
    fullname=models.CharField(max_length=200)
    email=models.EmailField(max_length=50)
    phone=models.IntegerField()
    gender=models.CharField(max_length=50)
    propic=models.ImageField(upload_to='images/')
    password=models.CharField(max_length=20)

class Sellproduct(models.Model):
    prodname=models.CharField(max_length=100)
    prodprice=models.IntegerField()
    proimg=models.ImageField('images/')
    prosize=models.CharField(max_length=200)
    desc=models.CharField(max_length=100)
    category=models.CharField(max_length=200)

    def __str__(self):
        return self.prodname

class Cart(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(Sellproduct,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    selected_size=models.CharField(max_length=20)



class Adressdet(models.Model):
    userdetails=models.ForeignKey(userregister,on_delete=models.CASCADE)
    adress1=models.CharField(max_length=200)
    adress2=models.CharField(max_length=200)
    pincode=models.IntegerField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    contact_name=models.CharField(max_length=20)
    contact_num=models.IntegerField()

class Wishpage(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(Sellproduct,on_delete=models.CASCADE)
    selected_size=models.CharField(max_length=20)

class Order(models.Model):
    userdetails=models.ForeignKey(userregister,on_delete=models.CASCADE)
    adress=models.ForeignKey(Adressdet,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    order_pic=models.ImageField(upload_to='image/')
    pro_name=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    status=models.BooleanField(default=True)


    
    

    
    




