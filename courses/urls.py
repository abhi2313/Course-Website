from django.contrib import admin
from django.shortcuts import HttpResponse
from django.urls import path,include
from courses.views import home,coursePage,signUpView,LoginView,signOut,checkOut,verify_payment,my_courses
from django.conf.urls.static import static
from django.conf import settings

from coursewebsite import settings
urlpatterns = [
    path('',home,name='home' ),
    path('signup',signUpView.as_view(),name='signup' ),
    path('login',LoginView.as_view(),name='login' ),
    path('logout',signOut,name='logout' ),
    path('my-courses',my_courses,name='my-courses' ),
    path('course/<str:slug>',coursePage,name='coursepage'),
    path('check-out/<str:slug>',checkOut,name='checkout'),
    path('verify_payment',verify_payment,name='verify_payment')
]+static(settings.MEDIA_URL,document_root=
settings.MEDIA_ROOT)

urlpatterns+=static(settings.STATIC_URL,document_root=
settings.STATIC_ROOT)