from django.urls import path

from user import views

urlpatterns = [
    path('', views.index),
    path('get_form/<str:cfn>/<str:ecn>', views.get_form),
    path('save_form/', views.save_form),
    path('end_form/', views.end_form),
    path('confirm_form/', views.save_form),
    path('is_census_nigth/', views.is_census_nigth),
    path('is_valid_code/<str:cfn>/<str:ecn>', views.is_valid_code),
]
