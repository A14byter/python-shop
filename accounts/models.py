from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()




class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    username=models.CharField(max_length=20)
    email=models.EmailField(blank=True ,  null= True)
    phone_number=models.CharField(max_length=11)
    password = models.CharField(max_length=50)
    date=models.DateTimeField( auto_now_add=True)

class AccountComplete(models.Model):
    account=models.OneToOneField(Account,on_delete=models.CASCADE)
    
    name=models.CharField(max_length=20)
    last_name= models.CharField(max_length=40)
    address=models.CharField(max_length=200)
    availbale_phone_number=models.CharField(max_length=11)
    post_code=models.CharField(max_length=15)
    nation_code=models.CharField(max_length=12)
    
class Notification(models.Model):
    WELCOME=1
    COMPLETE_ACCOUNT=2
    ADD_ITEM=3
    TRADE=4
    DELIVERY=5
    OFFER=7

    NOTIFICATION_TYPE_CHOICES=(
        (WELCOME, 'welcome'),
        (COMPLETE_ACCOUNT,'complete_account'),
        (ADD_ITEM,'add_item'),
        (TRADE, 'trade'),
        (DELIVERY,'delivery'),
        (OFFER,'offer')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    notification_type=models.PositiveSmallIntegerField(choices=NOTIFICATION_TYPE_CHOICES, default=WELCOME)
    text=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)




