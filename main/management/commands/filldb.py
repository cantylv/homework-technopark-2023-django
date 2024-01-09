from django.core.management.base import BaseCommand
from main.models import *

# Библиотека для генерации случайных данных
from faker import Faker
from faker.providers.lorem.en_US import Provider


class Command(BaseCommand):
    help = 'This script fills the default database with data.'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, help='Database fill factor.')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        if ratio is None:
            ratio = 1000

        generator = Faker('en_US')

        # User
        for i in range(ratio):
            user = User()
            user.password = generator.password(length=10)
            user.last_login = generator.date_time()
            user.is_superuser = False
            user.username = generator.unique.user_name()
            user.first_name = generator.first_name()
            user.last_name = generator.last_name()
            user.email = generator.unique.free_email()
            user.is_staff = False
            user.is_active = True
            user.date_reg = generator.date()
            user.rating = generator.pyint()
            user.date_joined = generator.date_time()
            user.save()
            # Profile
            profile = Profile()
            profile.user = user
            profile.avatar = 'users/user.jpg'
            profile.save()

        # Question
        for i in range(ratio*10):
            q = Question()
            q.title = generator.paragraph(nb_sentences=1)
            q.text = generator.paragraph(nb_sentences=5)
            # Получаем случайного пользователя из базы данных
            random_user = User.objects.order_by('?').first()
            q.date_create = generator.date()
            q.rating = generator.pyint(max_value=ratio)
            q.user = random_user
            q.save()

        # Answer
        for i in range(ratio*100):
            a = Answer()
            a.text = generator.paragraph(nb_sentences=5)
            a.date_create = generator.date()
            a.correct = generator.boolean(chance_of_getting_true=10)
            a.rating = generator.pyint(max_value=ratio)
            # Получаем случайного пользователя из базы данных
            random_user = User.objects.order_by('?').first()
            a.user = random_user
            # Получаем случайный вопрос из базы данных
            random_question = Question.objects.order_by('?').first()
            a.question = random_question
            a.save()

        # Tag
        for i in range(ratio):
            tag = Tag()
            tag.name = generator.word()
            tag.rating = generator.pyint()
            tag.save()

        # TagQuestion
        for i in range(ratio*10):
            unit = TagQuestion()
            unit.question = generator.pyint(min_value=1, max_value=100)
            unit.tag = generator.pyint(min_value=1, max_value=100)
            unit.save()

        # Likes
        for i in range(ratio*200):
            like_question = LikeQuestion()
            like_answer = LikeAnswer()

            random_user = User.objects.order_by('?').first()
            random_question = Question.objects.order_by('?').first()
            random_answer = Answer.objects.order_by('?').first()

            like_question.user = random_user
            like_question.question = random_question
            like_question.save()

            like_answer.user = random_user
            like_answer.answer = random_answer
            like_answer.save()

        # Dislikes
        for i in range(ratio * 200):
            dislike_question = DislikeQuestion()
            dislike_answer = DislikeAnswer()

            random_user = User.objects.order_by('?').first()
            random_question = Question.objects.order_by('?').first()
            random_answer = Answer.objects.order_by('?').first()

            dislike_question.user = random_user
            dislike_question.question = random_question
            dislike_question.save()

            dislike_answer.user = random_user
            dislike_answer.answer = random_answer
            dislike_answer.save()