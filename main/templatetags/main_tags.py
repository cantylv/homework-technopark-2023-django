from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_best_users():
    return Users.objects.order_by('-rating')[:10]  # Топ 10 пользователей


@register.simple_tag()
def get_user():
    return Users.objects.get(id=1)  # Выбираем пользователя, за чьим аккаунтом мы сидим (временно)


# Нужно будет еще сделать популярные теги
@register.simple_tag()
def get_popular_tags():
    return Tag.objects.all()[:10]
