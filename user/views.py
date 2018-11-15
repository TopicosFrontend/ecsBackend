from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from user.models import Code
from user.models import Section
from user.models import Item
from user.user_utils import save_form_data
from support.models import CensusNigth


from django.views.decorators.csrf import csrf_exempt
from ecsBackend.ecs_decorators import ecs_login_required
from ecsBackend.ecs_utils import read_json, string_to_json
from ecsBackend.ecs_authenticate import ecs_login, ecs_logout

import json
# salgado
def index(request):
    return HttpResponse("Hello from user backend")

# salgado
@csrf_exempt
def login(request):
    if ecs_login(request):
        return JsonResponse({"state": "true", "msg": "login successful"})
    else:
        return JsonResponse({"state": "false", "msg": "wrong user or password"})

# salgado
@csrf_exempt                                                                     
@ecs_login_required
def logout(request):                                                             
    if ecs_logout(request):
        return JsonResponse({"state": "true", "msg": "logout successful"})
    else:
        return JsonResponse({"state": "false", "msg": "error logout failed"})

# cristian
@csrf_exempt  
def get_form(request, cfn, ecn):
    res = []
    try:
        form = Code.objects.get(cfn=cfn, ecn=ecn).form
        sections = Section.objects.filter(form = form)
        for (i, iterator_section) in enumerate(sections):
            items_section = Item.objects.filter(section = iterator_section)
            res.append([])
            for iterator_items in items_section:
                res[i].append({'answer': iterator_items.answer})
        return JsonResponse({"state": True, "msg": "exito", "form": res})
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "form not found"})

# salgado
@csrf_exempt                                                                     
def save_form(request):
    form_json = string_to_json(request.body.decode("utf-8"))

    codes = form_json["codigo"]

    try:
        code = Code.objects.get(cfn=codes["cfn"], ecn=codes["ecn"])
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "form not found"})

    response = save_form_data(code.form, form_json)
    return JsonResponse(response)

# salgado
@csrf_exempt                                                                     
def end_form(request):
    data = string_to_json(request.body.decode("utf-8"))

    cfn = data["cfn"]
    ecn = data["ecn"]

    try:
        code = Code.objects.get(cfn=cfn, ecn=ecn)
        code.in_use = False
        code.save()
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "form not found"})
    except Exception:
        return JsonResponse({"state": "false", "msg": "error while finalizing form"})

    return JsonResponse({"state": "true", "msg": "Form finalized"})

#cristian
@csrf_exempt  
def is_census_nigth(request):
    try:
        register = CensusNigth.objects.get(pk = 1)
        return JsonResponse({"state": True, "msg": "Existe el registro", "is_census_nigth": register.isCensusNigth})
    except CensusNigth.DoesNotExist:
        return JsonResponse({"state": False, "msg": "No se ha iniciado el censo"})
    
