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
