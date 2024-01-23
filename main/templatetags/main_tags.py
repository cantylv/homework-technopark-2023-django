from django import template

from main.models import *
from django.core.cache import cache

register = template.Library()


# Нужно будет сделать с помощью cron-cкрипта
@register.simple_tag()
def get_popular_tags():
    return cache.get('popular_tags', [])


# Получение топ-10 пользователей с самыми популярными ответами
@register.simple_tag()
def get_best_users():
    return cache.get('best_users', [])


# вернуть id вопросов
@register.simple_tag()
def get_questions_likes(user):
    object_list = Question.objects.filter(likequestion__user=user) if user.is_authenticated else []
    return object_list


@register.simple_tag()
def get_questions_dislikes(user):
    object_list = Question.objects.filter(dislikequestion__user=user) if user.is_authenticated else []
    return object_list


# вернуть id ответов
@register.simple_tag()
def get_answers_likes(user):
    object_list = Answer.objects.filter(likeanswer__user=user) if user.is_authenticated else []
    return object_list


@register.simple_tag()
def get_answers_dislikes(user):
    object_list = Answer.objects.filter(dislikeanswer__user=user) if user.is_authenticated else []
    return object_list


# Правильный редирект в пагинаторе
def isQuestion(instance):
    if hasattr(instance[0], 'title'):
        return True
    return False


register.filter("isQuestion", isQuestion)
