"""
URL configuration for DjangoShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


from shoplist.views import ItemView,ItemDetailsview,ItemBoxView ,BuyItemView,DeliveryView
from accounts.views import SignUpView,LogInView,LogOutView,AccountCompleteView,NotificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',ItemView ,name='home'),
    path('signup/', SignUpView, name='signup'),
    path('login/',LogInView ,name='login'),
    path('logout/', LogOutView, name='logout'),
    path('home/itemdetails/<int:item_id>/', ItemDetailsview,name='item_details'),
    path('home/cart/',ItemBoxView, name='cart'),
    path('home/account-complete/',AccountCompleteView, name='account_complete'),
    path('buyitem/<int:item_id>/',BuyItemView,name='buy_item'),
    path('home/notifs/',NotificationView,name='notification'),
    path('home/delivery/',DeliveryView ,name='delivery')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
