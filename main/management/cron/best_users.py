from main.models import *
from django.db.models import Max, Value
from django.db.models.functions import Coalesce


# Этот cron-скрипт будет с заданным интервалом обновлять таблицу лучших пользователей
def updateBestUsers() -> None:
    # Вернется QuerySet из tuple
    top_users_questions = User.objects.annotate(
        rating=Coalesce(Max('question__rating'), Value(0))).order_by('-rating').select_related('profile')

    top_users_answers = User.objects.annotate(
        rating=Coalesce(Max('answer__rating'), Value(0))).order_by('-rating').select_related('profile')

    top_users = top_users_questions.union(top_users_answers).order_by('-rating')

    # Очищаем БД от старых значений
    if BestUsers.objects.all().count():
        BestUsers.objects.all().delete()

    users = []
    for user in top_users:
        if user not in users:
            users.append(user)
            BestUsers.objects.create(user=user)
        if len(users) == 10:
            break
