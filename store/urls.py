from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<category>[a-zA-Z0-9\s]+)?/$',views.storehome, name='storehome'),
    #path('/<str:cat>/',views.storehome, name='storehome-cat'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('reviews',views.reviews, name='reviews'),
    path('login',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('register',views.register_user, name='register_user'),
    path('product/<int:pk>', views.product, name='product'),
]
