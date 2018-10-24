from django.shortcuts import render, HttpResponse

# salgado
def index(request):
    return HttpResponse("Hello from collector backend")

# salgado
def login(request):
    return HttpResponse("collector login")

# silva
def generate_codes(request):
    return HttpResponse("collector generate_codes")

# silva
def get_info(request):
    return HttpResponse("collector get_info")

# silva
def notification(request):
    return HttpResponse("collector notification")
