from json import load as json_load, loads as json_loads

def code_to_json(code):
    return {"cfn": code.cfn, "ecn": code.ecn, "in_use": code.in_use}

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
    response["codigo"] = code_to_json(form.code)
    response["secciones"] = [section_to_json(section) for section in form.section_set.all()]
    return response

def read_json(json_file):
    with open("ecsBackend/data_files/%s" % json_file) as f:
        return json_load(f)

def string_to_json(string):
    return json_loads(string)
