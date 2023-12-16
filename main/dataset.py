from faker import Faker
from faker.providers.lorem.en_US import Provider
from .models import *

generator = Faker('en_US')


def fillUsers() -> None:
    for i in range(10000):
        user = Users()
        user.img = 'users/user.jpg'
        user.login = generator.unique.user_name()
        user.email = generator.unique.free_email()
        user.password = generator.password(length=10)
        user.date_reg = generator.date()
        user.rating = generator.pyint()
        user.save()


def fillQuestions() -> None:
    for i in range(100):
        q = Questions()
        q.title = generator.paragraph(nb_sentences=1)
        q.text = generator.paragraph(nb_sentences=5)
        # Получаем случайного пользователя из базы данных
        random_user = Users.objects.order_by('?').first()
        q.user = random_user
        q.date_create = generator.date()
        q.like = generator.pyint()
        q.dislike = generator.pyint()
        q.comment = generator.pyint()
        q.save()


def fillAnswers() -> None:
    for i in range(1000):
        a = Answers()
        a.text = generator.paragraph(nb_sentences=5)

        # Получаем случайного пользователя из базы данных
        random_user = Users.objects.order_by('?').first()
        a.user = random_user

        a.date_create = generator.date()
        a.like = generator.pyint()
        a.dislike = generator.pyint()
        a.correct = generator.boolean(chance_of_getting_true=25)

        # Получаем случайный вопрос из базы данных
        random_question = Questions.objects.order_by('?').first()
        a.question = random_question

        a.save()


def fillTags() -> None:
    for i in range(100):
        tag = Tag()
        tag.name = generator.word()
        tag.save()


def fillTagsQuestions() -> None:
    for i in range(300):
        unit = Tagquestions()
        unit.question_id = generator.pyint(min_value=1, max_value=100)
        unit.tag_id = generator.pyint(min_value=1, max_value=100)
        unit.save()

