from django.core.management.base import BaseCommand
from main.models import *

# Библиотека для генерации случайных данных
from faker import Faker

# Для получения случайных элементов
import random


class Command(BaseCommand):
    help = 'This script fills the default database with data.'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, help='Database fill factor.')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        if ratio is None:
            ratio = 1000

        generator = Faker('en_US')

        user_list = []
        profile_list = []
        # User and Profile
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
            user.date_joined = generator.date_time()
            user_list.append(user)

            # Profile
            profile = Profile()
            profile.user = user
            profile.avatar = 'users/user.jpg'
            profile_list.append(profile)

        # Удалять user_list не будем, потому что будем брать из него данные, а не в бд лазить
        User.objects.bulk_create(user_list)

        Profile.objects.bulk_create(profile_list)
        del profile_list

        print('_________Users were added_________')
        print('_________Profiles were added_________')

        tag_list = []
        # Tag
        for i in range(ratio):
            tag = Tag()
            tag.name = generator.word()
            tag.rating = generator.pyint(max_value=ratio * 10)
            tag_list.append(tag)

        Tag.objects.bulk_create(tag_list)
        print('_________Tags were added_________')

        question_list = []
        # Question
        for i in range(ratio * 10):
            q = Question()
            q.title = generator.paragraph(nb_sentences=1)
            q.text = generator.paragraph(nb_sentences=2)
            # Получаем случайного пользователя из базы данных
            # random_user = User.objects.order_by('?').first()

            # всего ratio пользователей, поэтому обращения к несуществующим данным не будет
            random_user = user_list[i % ratio]
            q.date_create = generator.date()
            q.rating = generator.pyint(max_value=ratio * 4)
            q.like = generator.pyint(max_value=ratio)
            q.dislike = generator.pyint(max_value=ratio)
            q.comment = generator.pyint(max_value=ratio)
            q.user = random_user
            question_list.append(q)

        # Удалять question_list не будем, потому что будем брать из него данные, а не в бд лазить
        Question.objects.bulk_create(question_list)
        # Теперь память под теги можно освободить
        del tag_list

        current_tag_id = 1
        for q in question_list:
            tag_number = random.randint(0, 3)
            q.tags.set(Tag.objects.filter(id__gte=current_tag_id).filter(id__lt=current_tag_id+tag_number))
            current_tag_id += tag_number
            current_tag_id %= ratio


        print('_________Questions were added_________')

        answer_list = []
        # Answer
        for i in range(ratio * 100):
            a = Answer()
            a.text = generator.paragraph(nb_sentences=2)
            a.date_create = generator.date()
            a.correct = generator.boolean(chance_of_getting_true=10)
            a.rating = generator.pyint(max_value=ratio * 4)
            a.like = generator.pyint(max_value=ratio)
            a.dislike = generator.pyint(max_value=ratio)
            # Получаем пользователя из списка
            random_user = user_list[i % ratio]
            a.user = random_user
            # Получаем случайный вопрос из базы данных
            random_question = question_list[i % ratio * 10]
            a.question = random_question
            answer_list.append(a)

        Answer.objects.bulk_create(answer_list)

        print('_________Answers were added_________')

        likeQuestion_list = []
        dislikeQuestion_list = []

        likeAnswer_list = []
        dislikeAnswer_list = []

        # Likes and Dislikes
        div_quest = ratio * 10  # кол-во вопросов
        div_ans = ratio * 100  # кол-во ответов
        for user in range(ratio):
            for i in range(1, 201):
                # Instances
                like_question = LikeQuestion()
                dislike_question = DislikeQuestion()

                like_answer = LikeAnswer()
                dislike_answer = DislikeAnswer()

                # Users
                user_like = user_list[user]
                user_dislike = user_list[ratio - user - 1]

                like_question.user = user_like
                dislike_question.user = user_dislike

                like_answer.user = user_like
                dislike_answer.user = user_dislike

                # Get Question from List
                question = question_list[(user + 1) * i % div_quest]

                # Get Answer From List
                answer = answer_list[(user + 1) * i % div_ans]

                # Fill Fields
                like_question.question = question
                dislike_question.question = question

                like_answer.answer = answer
                dislike_answer.answer = answer

                # Append into Lists
                likeQuestion_list.append(like_question)
                dislikeQuestion_list.append(dislike_question)

                # Answer
                likeAnswer_list.append(like_answer)
                dislikeAnswer_list.append(dislike_answer)

            if user % 1000 == 0:
                print(user)

        LikeQuestion.objects.bulk_create(likeQuestion_list)
        LikeAnswer.objects.bulk_create(likeAnswer_list)

        DislikeQuestion.objects.bulk_create(dislikeQuestion_list)
        DislikeAnswer.objects.bulk_create(dislikeAnswer_list)

        print('_________LikeQuestions were added_________')
        print('_________LikeAnswers were added_________')
        print('_________DislikeQuestions were added_________')
        print('_________DislikeAnswers were added_________')
        print('END')
