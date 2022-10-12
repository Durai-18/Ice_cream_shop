from django import views
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('hom', views.home, name = "hom" ),
    path('', views.signup_user, name = 'signup_user'),
    path('login', views.login, name = "login" ),
    path('login_request', views.login_request, name = "login_request" ),
    path('signup_userRegistration_output', views.signup_userRegistration_output, name = 'signup_userRegistration_output'),
    path('storeTotalSales',views.storeTotalSales,name='storeTotalSales'),
    path('monthWiseTotalSales',views.monthWiseTotalSales,name='monthWiseTotalSales'),
    path('mostPopularItem',views.mostPopularItem,name='mostPopularItem'),
    path('mostRevenue',views.mostRevenue,name='mostRevenue'),
    path('popularMaxMinAvg',views.popularMaxMinAvg,name='popularMaxMinAvg'),
    path('logout', views.logout, name = "logout" ),

]
