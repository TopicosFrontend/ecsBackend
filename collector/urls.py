from django.urls import path

from collector import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('generate_codes/', views.generate_codes),
    path('get_info/', views.get_info),
    path('notification/', views.notification),
]
