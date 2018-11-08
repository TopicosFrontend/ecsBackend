def code_to_json(code):
    return {"cfn": code.cfn, "ecn": code.ecn}

def collector_to_json(collector):
     response = {"id": collector.id, "user": collector.username, "nombre": collector.name}
     response["codes"] = [code_to_json(code) for code in collector.code_set.all()]
     return response   

def item_to_json(item):
    response = {}
    response["respuesta"] = item.question
    return response

def section_to_json(section):
    response = {}
    response["preguntas"] = [item_to_json(item) for item in section.item_set.all()]
    return response

def form_to_json(form):
    response = {}
    response["secciones"] = [section_to_json(section) for section in form.section_set.all()]
    return response
