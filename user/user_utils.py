from user.models import Form, Section, Item
from ecsBackend.ecs_utils import read_json

def create_item(section):
    item = Item(section=section)
    item.save()
    return item

def create_section(form, item_count):
    section = Section(form=form)
    section.save()

    for i in range(item_count):
        create_item(section)

    return section

def create_form(code):
    form_json = read_json("form_template.json")

    form = Form(code=code)
    form.save()

    for section_json in form_json["sections"]:
        create_section(form, section_json["items"])

    return form

def save_item_data(item, item_json):
    try:
        item.answer = item_json["respuesta"]
        item.save()
        return {"state": "true", "msg": "item saved"}
    except Exception:
        return {"state": "false", "msg": "error saving item"}

def save_section_data(section, section_json):
    try:
        items = section.item_set.all()
        items_json = section_json["preguntas"]

        for item, item_json in zip(items, items_json):
            response = save_item_data(item, item_json)
            if response["state"] is "false":
                return response
        return {"state": "true", "msg": "section saved"}
    except Exception:
        return {"state": "false", "msg": "error saving section"}

def save_form_data(form, form_json):
    try:
        sections = form.section_set.all()
        sections_json = form_json["secciones"]

        for section, section_json in zip(sections, sections_json):
            response = save_section_data(section, section_json)
            if response["state"] is "false":
                return response
        return {"state": "true", "msg": "form saved"}
    except Exception:
        return {"state": "false", "msg": "error saving form"}
