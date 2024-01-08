from django import template
from django.db.models import Max, Value
from django.db.models.functions import Coalesce

from main.models import *

register = template.Library()


@register.simple_tag()
def get_user():
    # return User.objects.get(id=1)  # Выбираем пользователя, за чьим аккаунтом мы сидим (временно)
    return User.objects.select_related('profile').get(id=1)


@register.simple_tag()
def get_popular_tags():
    return Tag.objects.order_by('-rating')[:10]


# Получение топ-10 пользователей с самыми популярными ответами
@register.simple_tag()
def get_best_users():
    # Вернется QuerySet из tuple
    top_users_questions = User.objects.annotate(
        rating=Coalesce(Max('question__rating'), Value(0))).order_by('-rating').select_related('profile')[:10]

    for u in top_users_questions:
        print(u.pk, u.username, u.rating)

    print('______________')
    top_users_answers = User.objects.annotate(
        rating=Coalesce(Max('answer__rating'), Value(0))).order_by('-rating').select_related('profile')[:10]

    for u in top_users_answers:
        print(u.pk, u.username, u.rating)

    print('______________')

    top_users = top_users_questions.union(top_users_answers).order_by('-rating')

    for u in top_users_answers:
        print(u.pk, u.username, u.rating)

    users = []
    for user in top_users:
        if user not in users:
            users.append(user)
        if len(users) == 10:
            break

    return users


################################################################

# Question
@register.simple_tag()
def get_question_like(q_id):
    return LikeQuestion.objects.filter(question=q_id).count()


@register.simple_tag()
def get_question_dislike(q_id):
    return DislikeQuestion.objects.filter(question=q_id).count()


@register.simple_tag()
def get_question_ans(q_id):
    return Answer.objects.filter(question=q_id).count()


@register.simple_tag()
def get_question_tags(q_id):
    result_tags = []
    tags = Tag.objects.select_related('tagquestion').filter(tagquestion__question_id=q_id).values_list('name')
    for tag in tags:
        result_tags.append(tag[0])
    return result_tags


################################################################

# Answer
@register.simple_tag()
def get_answer_like(ans_id):
    return LikeAnswer.objects.filter(answer=ans_id).count()


@register.simple_tag()
def get_answer_dislike(ans_id):
    return DislikeAnswer.objects.filter(answer=ans_id).count()
