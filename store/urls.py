from django.urls import path
from . import views

urlpatterns = [
    path('',views.storehome, name='storehome'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('reviews',views.reviews, name='reviews'),
    path('login',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('register',views.register_user, name='register_user'),
    path('product/<int:pk>', views.product, name='product'),
]
