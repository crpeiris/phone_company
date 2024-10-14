from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('',views.storehome, name='storehome'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('reviews',views.reviews, name='reviews'),
    path('login',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('register',views.register_user, name='register_user'),
    path('shop',views.shop, name='shop'),
    path('shop/<str:category>/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product, name='product'),
]
urlpatterns += staticfiles_urlpatterns()
 