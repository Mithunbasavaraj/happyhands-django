from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# products 
class product(models.Model):
   product_name = models.CharField(max_length=255)
   quantity = models.IntegerField(default=0,blank=True,)
   product_description =models.TextField(blank=True,default="")
   specifications =models.TextField(blank=True,default="")
   price=models.IntegerField(default=0,blank=True)
   strikeout_price=models.IntegerField(default=0,blank=True)
   image_1=models.ImageField(upload_to='products/' ,blank=True,)
   image_2=models.ImageField(upload_to='products/' ,blank=True,)
   image_3=models.ImageField(upload_to='products/' ,blank=True,)
   image_4=models.ImageField(upload_to='products/' ,blank=True,)
   image_5=models.ImageField(upload_to='products/' ,blank=True,)
   image_6=models.ImageField(upload_to='products/' ,blank=True,)
   image_7=models.ImageField(upload_to='products/' ,blank=True,)
   key_words=models.CharField(max_length=255,blank=True,default="")
   juice_type =models.CharField(max_length=255,blank=True,default="")
   category =models.CharField(max_length=255,blank=True,default="")
   slug= models.SlugField(blank=True,default="")

   def __str__(self):
       return self.product_name
   

  

# cart model
class cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    unit_qty= models.IntegerField(default=0,blank=True,)
    amount  = models.IntegerField(default=0,blank=True,)

    def __str__(self):
       return self.user

payment_choice=(
    ("online","online"),
    ("cod","cod")
)

Order_status_choices=(
    ("Pending","Pending"),
    ("Order placed","Order placed"),
    ("Order conformed","Order conformed"),
    ("Processing","Processing"),
    ("Ready to ship","Ready to ship"),
    ("Dispatched","Dispatched"),
    ("Completed","Completed"),
)
# order model
class order(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   payment_type= models.CharField( max_length=10,choices=payment_choice,default="")
   total_price  = models.IntegerField(default=0,blank=True,)
   date = models.DateTimeField( default=datetime.now)
   name=models.CharField(max_length=55, default="", blank=True)
   phone=models.CharField(max_length=25, default="", blank=True)
   email=models.CharField(max_length=35, default="", blank=True)
   house_no=models.CharField(max_length=35, default="", blank=True)
   area=models.CharField(max_length=35, default="", blank=True)
   city=models.CharField(max_length=35, default="", blank=True)
   state=models.CharField(max_length=35, default="", blank=True)
   pin_code=models.CharField(max_length=15, default="", blank=True)
   landmark=models.CharField(max_length=35, default="", blank=True)
   Order_status=models.CharField(max_length = 20, choices = Order_status_choices, default = 'Pending') 
   payment_status=models.CharField(max_length=35, default="", blank=True)
   j_cart_product = models.IntegerField(default=0,blank=True)
   uuid=models.CharField(max_length=135, default="", blank=True)
   transaction_id=models.CharField(max_length=135, default="", blank=True)

   def __str__(self):
       return self.user

