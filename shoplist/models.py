from django.db import models
from accounts.models import Account
from django.contrib.auth import get_user_model
from django.conf import settings
User=get_user_model()

class ItemList(models.Model):
    title = models.CharField(max_length=20)
    describetion=models.TextField(max_length=300)
    image=models.ImageField()
    price=models.FloatField(null=True)
    off_price=models.FloatField(null=True)
    date=models.DateTimeField(auto_now=True)
    review=models.TextField(blank=True,null=True)
    
    
    class Meta:
        verbose_name ='Items'



class Trade(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    item_box=models.BooleanField(default=False)
    item_bought=models.BooleanField(default=False)

    class Meta:
        verbose_name ='trades'


class Comment(models.Model):
    item=models.ForeignKey(ItemList,on_delete=models.CASCADE)
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    text=models.TextField(max_length=200, blank=True, null=True)
    rate=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    confirm=models.BooleanField(default=True)

    class Meta:
        verbose_name='comments'

class Delivery(models.Model):
    trade=models.ForeignKey(Trade,on_delete=models.CASCADE)
    accepted=models.BooleanField(default=False)
    post=models.BooleanField(default=False)
    delievered=models.BooleanField(default=False)
    

