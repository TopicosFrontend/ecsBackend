from django.urls import path

from user import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('get_form/<str:cfn>/<str:ecn>', views.get_form),
    path('save_form/', views.save_form),
    path('end_form/', views.end_form),
    path('confirm_form/', views.save_form),
]
