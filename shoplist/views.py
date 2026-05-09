from django.shortcuts import render, redirect
from .models import ItemList
from .models import Trade , Comment ,Delivery
from accounts.models import Account, AccountComplete, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django.core.cache import cache

from collections import Counter
import secrets
import string

User=get_user_model()

@login_required(login_url='login')
def ItemView(request):
    existness=None
    user=request.user
    
    
    item_object = ItemList.objects.all()

    item_name = request.GET.get('item_name')
    

    if item_name!='' and item_name is not None:
        
        item_object=ItemList.objects.filter(title__icontains=item_name)

        
    if request.method == 'POST':

        item_add=request.POST.get('item_add')

        
    
        item=get_object_or_404(ItemList,title=item_add
            )

        existness=Trade.objects.filter(
            user = request.user,
            item= item,
            item_box=True, )
        if not existness and item_add:

            Trade.objects.create(
                user=request.user,
                item=item,
                item_box=True
            )
            Notification.objects.create(
                user=user,
                notification_type=3,
                text='1 item has been added to box.'


            )

            
        elif existness and item_add:
            existness.delete()

        return redirect('home')        



    existness_list=[]

    for current_item in item_object:
        
        existness_check=Trade.objects.filter(
            user=request.user,
            item=current_item,
            item_box=True
            ).first()
        if existness_check:   
            existness_list.append(existness_check.item)
    
        
    return render(request ,'shoplist/index.html' ,{'item_object':item_object,'existness_list':existness_list})


@login_required(login_url='login')
def ItemDetailsview(request, item_id):
    existness=None
    error=None

    user=request.user
    account=Account.objects.filter(user=user).first()
    
    item = ItemList.objects.filter(id=item_id).first()
    comments = Comment.objects.filter(item=item)
    


    if request.method == 'POST':
        request_name=request.POST.get('request_name')

        if request_name == 'item':

            item_add_name=request.POST.get('item_add_name')
            item_add=get_object_or_404(ItemList,title=item_add_name
            )

            existness=Trade.objects.filter(
                user = request.user,
                item= item_add,
                item_box=True, ).first()

            if not existness and item_add_name:
                Trade.objects.create(
                    user=request.user,
                    item=item_add,
                    item_box=True
                )
            
            elif existness and item_add_name:
                existness.delete()

            return redirect('item_details',item_id=item_id)


        if request_name == 'comment':
            rate=request.POST.get('rate')
            comment=request.POST.get('comment')

            if not rate=='' and rate is not None:
                if not Trade.objects.filter(user=user,
                    item=item,
                    item_bought=True).exists():

                    error='sorry , you cant rate this item before buying it.'

                else:
                    
                    Comment.objects.create(
                        item=item,
                        account=account,
                        text=comment,
                        rate=rate)
                    return redirect('item_details',item_id=item_id)
                    
            else:
                error='please rate the item.'
            

        

    existness=Trade.objects.filter(
        user = request.user,
        item= item,
        item_box=True, ).first()
    
    return render(request , 'shoplist/index2.html', {'item': item , 'existness':existness,'comments':comments, 'error':error})


@login_required(login_url='login')
def ItemBoxView(request):
    id_list=[]

    count=0

    price_list=[]
    total_price=0

    off_list=[]
    total_off=0

    user=request.user
    box_list=Trade.objects.filter(
        user=user,
        item_box=True,
        item_bought=False
        )
   
   

    bought_list=Trade.objects.filter(
        user=user,
        item_bought=True
    )

    for trade in box_list:
        price_list.append(trade.item.price)
    
    for price in price_list:
        count+=1
    
    for price in price_list:
        total_price+=price
    
    for trade in box_list:
        if trade.item.off_price:
            off_list.append(trade.item.off_price)
        else:
            off_list.append(trade.item.price)
        
    for price in off_list:
        total_off+=price

    for trade in box_list:
        id_list.append(trade.item.id)


    if request.method =='POST':
        buy_all=request.POST.get('buy_all')


        request.session["id_list"]=id_list
        return redirect('buy_item',1)


    return render(request,'shoplist/index3.html' ,{'box_list':box_list, 'bought_list':bought_list,'count':count,'total_price':total_price,'total_off':total_off})




@login_required(login_url='login')
def BuyItemView(request, item_id):
    complete_error=None
    error=None
    code=None

    

    user=request.user
    item=ItemList.objects.get(id=item_id)
    account=Account.objects.filter(user=user).first()
    account_complete=AccountComplete.objects.filter(account=account).first()

    id_list=request.session.get('id_list',[])
    all_items=ItemList.objects.filter(id__in=id_list)




    if not AccountComplete.objects.filter(account=account).exists() :
        complete_error='you must complete the informations first.'

    
    if not request.session.session_key:
        request.session.create()
    
    cache_key = f"verification_code_{request.session.session_key}"
    code = cache.get(cache_key)
    
    if code is None:
        
        characters = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(characters) for _ in range(6))
        cache.set(cache_key, code, 300)

    if not code:
        error='token has been expired, please refresh the page .'

    if request.method=='POST':
        
        code_check=request.POST.get('code_check')


        if code_check==code :
            Notification.objects.create(
                user=user,
                notification_type=4,
                text='thanks for your trade. you can check delivery prosscs each time.'
            )
            if not all_items :
                trade=Trade.objects.filter(user=user,item=item, item_box=True).first()
                Trade.objects.filter(user=user, item=item).update(item_bought=True, item_box=False)
                trade=Trade.objects.filter(user=user,item=item,item_bought=True, item_box=False).first()

                Delivery.objects.create(trade=trade,
                                        accepted=True)

                cache.delete(cache_key)
                error='succesfull payment.'
                return redirect('cart')
                
            else:
                trades=Trade.objects.filter(user=user, item_box=True)

                for t in trades:
                    Delivery.objects.create(trade=t,accepted=True)

                Trade.objects.filter(user=user,item_box=True).update(item_bought=True,item_box=False)
                
                error='succesfull payment.'
                

                    
                cache.delete(cache_key)
                return redirect('cart')

        else:
            cache.delete(cache_key)
            error='the payment validation failed.'

    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(6))
    cache.set(cache_key, code, 300)
    
    return render(request,'shoplist/index4.html',{'code':code,'error':error ,'complete_error':complete_error})

    
@login_required(login_url='login')
def DeliveryView(request):
    error=None
    delivery_information=[]
    
    user=request.user
    account=Account.objects.filter(user=user).first()
   
    trades=Trade.objects.filter(user=user , item_bought=True)
    if not trades:
        error='you had not delivered any item yet.'

    account_complete=AccountComplete.objects.filter(account=account).first()
    for trade in trades:
        delivery=Delivery.objects.filter(trade=trade).first()
        delivery_information.append(delivery)

    return render(request,'shoplist/index5.html',{'account_complete':account_complete ,'delivery_information':delivery_information ,'error':error})

    







    
    
    
    