from django.urls import path
from .views import homepage,register,logout_request,login_request,single_slug


urlpatterns = [

    path('',homepage,name='homepage'),
    path('register/',register,name='register'),
    path('logout/',logout_request,name='logout'),
    path('login/',login_request,name='login'),
    path('<single_slug>',single_slug,name='single_slug'),



]


