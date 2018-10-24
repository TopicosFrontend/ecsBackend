from django.shortcuts import render, HttpResponse

# salgado
def index(request):
    return HttpResponse("Hello from user backend")

# salgado
def login(request):
    return HttpResponse("user login")

# cristian
def get_form(request):
    return HttpResponse("user get_form")

# salgado
def save_form(request):
    return HttpResponse("user save_form")

# salgado
def end_form(request):
    return HttpResponse("user end_form")

# cristian
def confirm_form(request):
    return HttpResponse("user confirm_form")
