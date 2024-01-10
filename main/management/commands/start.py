# Скрипт, который восстановит актуальные значения лайков и дизлайков в системе
from main.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'This script fills the default database with correct data. Need only in the start.'

    def handle(self, *args, **kwargs):
        # question_list = Question.objects.all()
        for index, q in enumerate(Question.objects.all()):
            q.like = q.likequestion_set.count()
            q.dislike = q.dislikequestion_set.count()
            q.comment = q.answer_set.count()
            q.countRating()
            q.save()

        print('questions done')
        # Question.objects.bulk_update(question_list, ['like', 'dislike', 'comment', 'rating'])

        # answer_list = Answer.objects.all()
        for index, a in enumerate(Answer.objects.all()):
            a.like = a.likeanswer_set.count()
            a.dislike = a.dislikeanswer_set.count()
            a.countRating()
            a.save()

        # Answer.objects.bulk_update(answer_list, ['like', 'dislike', 'rating'])

        print('answers done')