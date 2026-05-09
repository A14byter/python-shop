from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from .models import Account,AccountComplete,Notification
from django.contrib.auth.decorators import login_required
import re


User=get_user_model()

def SignUpView(request):
    signup_error=None
    if request.method== "POST":

        phone_number=request.POST.get('phone_number')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
    
        if  phone_number is None or phone_number=='' or username=='' or password=='' or confirm_password=='' :
            signup_error='required fields cant be empty '
        

        elif  phone_number  and len(phone_number)!=11 :
            signup_error='enter A valid phone number.'

        elif Account.objects.filter(phone_number=phone_number).exists() :
        
            signup_error='A user with this phone number exists, please log in'
    
        elif  email !='' and  not ( '@' and '.com') in email  :
            signup_error='enter A valid Email'
    
        elif Account.objects.filter(username=username).exists():
            signup_error='this username being used, choose another username. '
     
        elif password!=confirm_password:
            signup_error='passwords are not match'
    
        elif password and confirm_password and len(password)<8 :
            signup_error='password must be at least 8 characters, better use multiple chracters.'
        else:

            hashed_password=make_password(password)

           
            user=User.objects.create_user(
            
                username=username,
                email=email,
                password=password
            )

            Account.objects.create(
                user=user,
                phone_number=phone_number,
                username=username,
                email=email,
                password=hashed_password
            )
            login(request, user)
            Notification.objects.create(
                user=user,
                notification_type=1,
                text='Wellcome to the StarkS Shop, our Goal is to show you best items with best offers.'

            )


            Notification.objects.create(
                user=user,
                notification_type=2,
                text='please complete your information so you can deliver item .'
            )

            signup_error='Account sucessfully has been created'
    return render(request ,'accounts/index.html' ,{'signup_error':signup_error})



def LogInView(request):
    login_error=None

    if request.method == "POST":
        phone_number = request.POST.get('phone_number').strip()
        password = request.POST.get('password')
        try :
            int(phone_number)
            valid=True
        except ValueError:
            valid=False

        if phone_number is None or phone_number=='' or password=='':
            login_error='reqired fields can not be empty'


        elif  not phone_number.isdigit() or len(phone_number)!=11 :
            login_error = 'enter a valid phone number'

        
    
        
        elif not valid:
            login_error='enter a valid phone number'
        else:

            account=Account.objects.filter(phone_number=phone_number).first()

            account_username=account.username

            user=User.objects.filter(username=account_username).first()

            if user:
                if check_password(password , user.password):
                    user=User.objects.filter(
                                    username=account_username).first()
                    
                    login(request, user)
                    return redirect('home')
                else:
                    login_error='the password is not correct.'
    
            else:
                login_error='user does not exists, please sign up.'

    return render(request,'accounts/index2.html', {'login_error':login_error})


def LogOutView(request):
    logout_error=None
    
    
    if  request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else: 
        return redirect('signup')

@login_required(login_url='login')
def AccountCompleteView(request):
    account_complete=None
    error=None
    confirm=None
    succes=None
    int_check=None
    


    user=request.user 
    account=Account.objects.get(user=user)

    if AccountComplete.objects.filter(account=account).exists():
        account_complete=AccountComplete.objects.filter(account=account).first()
    else:
        confirm=' you must enter the required informations'
    
    if request.method =='POST' :


        name=request.POST.get('name')
        last_name=request.POST.get('last_name')

        address=request.POST.get('address')
        availbale_phone_number=request.POST.get('availbale_phone_number')
        post_code=request.POST.get('post_code')
        nation_code=request.POST.get('nation_code')
        

        pattern=  r'^[a-zA-Z]+$'


        name_check=bool(re.match(pattern,name))
        last_name_check=bool(re.match(pattern,last_name))

        fields_to_check = [name, last_name, address, availbale_phone_number, post_code, nation_code]
        
        try:
           int_check= int(availbale_phone_number)+ int(post_code) + int(nation_code)

        except ValueError:
            pass
        
        if int_check is None:
            error='please enter valid informations'
    

        elif any(field is None or field.strip() == "" for field in fields_to_check):
            error='please enter valid informations'
        

        elif name_check is False or last_name_check is False:
            error='please enter valid informations'
        
        else:
            if AccountComplete.objects.filter(account=account).exists():

                AccountComplete.objects.filter(account=account).update(
                name=name,
                last_name=last_name,
                address=address,
                availbale_phone_number=availbale_phone_number,
                post_code=post_code,
                nation_code=nation_code
            )
                succes='your information has been updated succesfuly.'

            else:

                account_complete=AccountComplete.objects.get_or_create(
                    account=account,
                name=name,
                last_name=last_name,
                address=address,
                availbale_phone_number=availbale_phone_number,
                post_code=post_code,
                nation_code=nation_code,
            )

                succes='your information has been added successfuly.'
            
            
    account_complete=AccountComplete.objects.filter(account=account).first()

    return render(request,'accounts/index3.html',{'error':error,'confirm':confirm ,'succes':succes,'account_complete':account_complete})


@login_required(login_url='login')    
def NotificationView(request):
    error=None
    
    
    user=request.user
    notification=Notification.objects.filter(user=user)
    if not Notification:
        error='Notifications will be showed here.'

    

    

    if request.method == 'POST':
        notif_id=request.POST.get('notif_id')
        target_notif=Notification.objects.filter(id=notif_id).first()
        target_notif.delete()
        return redirect('notification')
    

    return render(request,'accounts/index4.html',{'notification':notification,'error':error})

    
    

        

        








        
        

    



       

      
    

    

    


    
    
    


    

