from django.http import JsonResponse

def ecs_login_required(method):
    def ecs_decorator(request):
        if not request.user.is_authenticated:
            return JsonResponse({"state": "false", "msg": "user is not logged in"})
        return method(request)
    return ecs_decorator
