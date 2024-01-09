from django import template
from django.db.models import Max, Value
from django.db.models.functions import Coalesce

from main.models import *

register = template.Library()


@register.simple_tag()
def get_user():
    # return User.objects.get(id=1)  # Выбираем пользователя, за чьим аккаунтом мы сидим (временно)
    return User.objects.select_related('profile').get(id=1)


# Нужно будет сделать с помощью cron-cкрипта
@register.simple_tag()
def get_popular_tags():
    return Tag.objects.order_by('-rating')[:10]


# Получение топ-10 пользователей с самыми популярными ответами
@register.simple_tag()
def get_best_users():
    # Вернется QuerySet из tuple
    top_users_questions = User.objects.annotate(
        rating=Coalesce(Max('question__rating'), Value(0))).order_by('-rating').select_related('profile')[:10]

    top_users_answers = User.objects.annotate(
        rating=Coalesce(Max('answer__rating'), Value(0))).order_by('-rating').select_related('profile')[:10]

    top_users = top_users_questions.union(top_users_answers).order_by('-rating')

    users = []
    for user in top_users:
        if user not in users:
            users.append(user)
        if len(users) == 10:
            break

    return users
