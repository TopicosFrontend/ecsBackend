from django.http import JsonResponse

from support.models import SupportInfo
from collector.models import CollectorInfo

def ecs_login_required(method):
    def ecs_decorator(request):
        if not request.user.is_authenticated:
            return JsonResponse({"state": "false", "msg": "user is not logged in"})
        return method(request)
    return ecs_decorator

def ecs_support_only(method):
    def ecs_decorator(request):
        try:
            username = request.user.get_username()
            user_support = SupportInfo.objects.get(username=username)
            return method(request)
        except SupportInfo.DoesNotExist:
            return JsonResponse({"state": "false", "msg": "user is not a support member"})
    return ecs_decorator

def ecs_collector_only(method):
    def ecs_decorator(request):
        try:
            username = request.user.get_username()
            user_support = CollectorInfo.objects.get(username=username)
            return method(request)
        except CollectorInfo.DoesNotExist:
            return JsonResponse({"state": "false", "msg": "user is not a collector member"})
    return ecs_decorator
