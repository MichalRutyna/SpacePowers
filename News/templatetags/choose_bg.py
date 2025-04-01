from django import template

register = template.Library()

@register.simple_tag()
def choose_bg(roll):
    if roll == 1:
        bg = "bg-black"
    elif roll <= 4:
        bg = "bg-danger"
    elif roll <= 8:
        bg = "bg-warning"
    elif roll <= 13:
        bg = "bg-light"
    elif roll <= 18:
        bg = "bg-success"
    elif roll <= 20:
        bg = "bg-info"
    else:
        return None
    return bg


register.simple_tag(choose_bg, name="choose_bg")