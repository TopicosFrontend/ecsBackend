from django.shortcuts import HttpResponse

from django.http import JsonResponse

from user.models import Code, Section, Item
from support.models import CensusNigth

from django.views.decorators.csrf import csrf_exempt
from ecsBackend.ecs_decorators import ecs_login_required
from ecsBackend.ecs_json_utils import string_to_json
from ecsBackend.ecs_authenticate import ecs_login, ecs_logout

from user.user_utils import save_form_data

import json
# salgado
def index(request):
    return HttpResponse("Hello from user backend")

# cristian
@csrf_exempt  
def get_form(request, cfn, ecn):
    res = []
    try:
        form = Code.objects.get(cfn=cfn, ecn=ecn).form
        sections = Section.objects.filter(form = form)
        for i, iterator_section in enumerate(sections):
            items_section = Item.objects.filter(section = iterator_section)
            res.append([])
            for iterator_items in items_section:
                res[i].append({'answer': iterator_items.answer})
        return JsonResponse({"state": True, "msg": "exito", "form": res}, safe=False)
    except Code.DoesNotExist:
        return JsonResponse({"state": False, "msg": "form not found"}, safe=False)

# salgado
@csrf_exempt                                                                     
def save_form(request):
    form_json = string_to_json(request.body.decode("utf-8"))

    codes = form_json["codigo"]

    try:
        code = Code.objects.get(cfn=codes["cfn"], ecn=codes["ecn"])
    except Code.DoesNotExist:
        return JsonResponse({"state": False, "msg": "form not found"}, safe=False)

    response = save_form_data(code.form, form_json)
    return JsonResponse(response, safe=False)

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
        return JsonResponse({"state": False, "msg": "form not found"}, safe=False)
    except Exception:
        return JsonResponse({"state": False, "msg": "error while finalizing form"}, safe=False)

    return JsonResponse({"state": True, "msg": "Form finalized"}, safe=False)

#cristian
@csrf_exempt  
def is_census_nigth(request):
    try:
        register = CensusNigth.objects.get(pk = 1)
        return JsonResponse({"state": True, "msg": "Existe el registro", "is_census_nigth": register.isCensusNigth}, safe=False)
    except CensusNigth.DoesNotExist:
        return JsonResponse({"state": False, "msg": "No se ha iniciado el censo"}, safe=False)
    
@csrf_exempt
def is_valid_code(request, cfn, ecn):
    try:
        Code.objects.get(cfn = cfn, ecn = ecn)
        return JsonResponse({"state": True, "msg": "Existe el registro"}, safe=False)
    except Code.DoesNotExist:
        return JsonResponse({"state": False, "msg": "No existe el formulario asociado a los codigos"}, safe=False)
