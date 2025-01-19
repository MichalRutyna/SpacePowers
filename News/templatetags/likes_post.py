from django import template

register = template.Library()


@register.simple_tag()
def likes_post(user, post):
    return post.is_liked_by(user)

register.simple_tag(likes_post, name="likes_post")