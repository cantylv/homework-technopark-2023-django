from django import template

from main.models import *

register = template.Library()


@register.simple_tag()
def get_user():
    # return User.objects.get(id=1)  # Выбираем пользователя, за чьим аккаунтом мы сидим (временно)
    return User.objects.select_related('profile').get(id=1)


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
