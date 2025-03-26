from django import template

register = template.Library()


@register.simple_tag()
def owner_title(nation, user):
    return nation.get_title_of_user(user)

register.simple_tag(owner_title, name="owner_title")