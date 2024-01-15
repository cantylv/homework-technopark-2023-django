from django import template

from main.models import *

register = template.Library()


# Нужно будет сделать с помощью cron-cкрипта
@register.simple_tag()
def get_popular_tags():
    return Tag.objects.order_by('-rating')[:20]


# Получение топ-10 пользователей с самыми популярными ответами
@register.simple_tag()
def get_best_users():
    return BestUsers.objects.all()[:10]


# Правильный редирект в пагинаторе
def isQuestion(instance):
    if hasattr(instance[0], 'title'):
        return True
    return False


register.filter("isQuestion", isQuestion)
