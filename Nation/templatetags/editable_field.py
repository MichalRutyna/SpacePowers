from django import template

register = template.Library()


@register.inclusion_tag("nation/components/editable_field.html")
def editable_field(context):
    return ""


register.simple_tag(editable_field, name="editable_nation_field")