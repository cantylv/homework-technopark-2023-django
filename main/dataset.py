from faker import Faker
from faker.providers.lorem.en_US import Provider
from .models import *


def fillUsers() -> None:
    for i in range(10000):
        generator = Faker('en_US')
        user = Users()
        user.img = 'users/fitness.img'
        user.login = generator.unique.user_name()
        user.email = generator.unique.free_email()
        user.password = generator.password(length=10)
        user.date_reg = generator.date()
        user.rating = generator.pyint()
        user.save()


def fillQuestions() -> None:
    for i in range(100):
        generator = Faker('en_US')
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