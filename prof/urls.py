from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('getCourseList', views.getCourseList),
    path('createLecInstance', views.createLecInstance),
    path('delLecInstance', views.delLecInstance),
    path('getQR', views.getQR),
    path('getStats', views.getStats),
]
