from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def ecs_login(request):
    data = request.POST
    username = data["user"]
    password = data["password"]

    user = authenticate(username=username, password=password)

    if user is None:
        return False
    else:
        auth_login(request, user)
        return True

def ecs_logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
        return False
    else:
        return True
