from django.shortcuts import render, HttpResponse

# salgado
def index(request): 
    return HttpResponse("Hello from support backend")

# salgado
def login(request):
    return HttpResponse("support login")

# salgado
def register(request):
    return HttpResponse("support register")

# salgado
def show_collector(request):
    return HttpResponse("support show_collector")

# salgado
def show_collectors(request):
    return HttpResponse("support show_collectors")

# salgado
def show_form(request):
    return HttpResponse("support show_form")

# silva
def census_status(request):
    return HttpResponse("support census_status")

# unassigned
def transfer_forms(request):
    return HttpResponse("support transfer_forms")

# salgado
def register_collectors(request):
    return HttpResponse("support register_collectors")

# silva
def set_population(request):
    return HttpResponse("support set_population")

# salgado
def start_census_night(request):
    return HttpResponse("support start_census_night")
