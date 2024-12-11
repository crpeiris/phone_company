from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('search_product/', views.search_product, name='search_product'),
    path('get_product/', views.get_product, name='get_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),  # Corrected URL pattern
    
    path('view_orders/', views.view_orders, name='view_orders'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('', views.staff_dashboard, name='staff_dashboard'),
]
