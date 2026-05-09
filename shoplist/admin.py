from django.contrib import admin

from .models import ItemList,Trade,Comment,Delivery

class ItemListAdmin(admin.ModelAdmin):
    list_display=['id','title' ,'describetion','image','date']
    list_filter =['title' , 'date']
    search_fields=['title']
    verbose_name = 'title'

class TradeAdmin(admin.ModelAdmin):
        list_display = ('user', 'item', 'item_box', 'item_bought')


admin.site.register(ItemList , ItemListAdmin)
admin.site.register(Trade,TradeAdmin)
admin.site.register(Comment)
admin.site.register(Delivery)



