from django import template

register = template.Library()

@register.filter(name='addid')
def addid(field, id):
   return field.as_widget(attrs={"id":id, "class": "form-control"})
