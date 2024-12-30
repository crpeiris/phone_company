from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_home, name='staff_home'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/', views.edit_product, name='edit_product'),
    path('get_product/', views.get_product, name='get_product'),  # For AJAX product search
    path('search_product_list/', views.search_product_list, name='search_product_list'),  # For dynamic search
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('view_order/', views.view_order, name='view_order'),
]
