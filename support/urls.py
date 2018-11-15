from django.urls import path

from support import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('show_collector/', views.show_collector),
    path('show_collectors/', views.show_collectors),
    path('show_form/', views.show_form),
    path('census_status/', views.census_status),
    path('transfer_forms/', views.transfer_forms),
    path('register_collectors/', views.register_collectors),
    path('start_census/', views.start_census),
    path('start_census_night/', views.start_census_night)
]
