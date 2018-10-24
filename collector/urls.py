from django.urls import path

from collector import views

urlpatterns = [
    path('', views.index)
]
