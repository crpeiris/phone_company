from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('',views.cart_summary, name='cart_summary'),
    path('add/',views.cart_add, name='cart_add'),
    #path('delete/',views.cart_delete, name='cart_delete'),
    #path('update',views.cart_update, name='cart_update'),
]
urlpatterns += staticfiles_urlpatterns()
 