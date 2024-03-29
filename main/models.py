from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Нужно будет добавить красивую админ-панель
# Словарь, который содержит вес параметра оценки рейтинга в моей системе
weightParam = {
    'like': 4,
    'dislike': 1,
    'comment': 2
}


# У нас есть готовая модель User-а (django.contrib.auth.models.User)
# Создадим модель Profile, чтобы дополнить модель User аватаркой пользователя
# Вообще я бы так не делал, но это функциональное требование системы
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    avatar = models.ImageField(upload_to='users/')

    class Meta:
        managed = True
        db_table = 'Profile'


# Связь многие-ко-многим с сущностью Question
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    # можем проиндексировать, потому что менять рейтинг тега мы будем с помощью cron-скрипта не так часто
    rating = models.IntegerField(null=True, default=0, db_index=True)

    class Meta:
        managed = True
        db_table = 'Tag'


class ManagerQuestion(models.Manager):
    def getNewestQuestions(self):
        return self.order_by('-date_create')

    def getPopularQuestions(self):
        return self.order_by('-rating')

    # Нужно будет добавить проверку на уникальность строки данных.
    # Сейчас пользователь может добавить много лайков к вопросу
    def getQuestionsByTag(self, tags):  # tags - строка, содержащая теги, разделенные символом @
        tags = tags.split('@')  # получили массив тегов
        return self.filter(tags__name__in=tags), tags


# Нужно добавить в модель систему рейтинга
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    rating = models.IntegerField(null=True, default=0)
    like = models.IntegerField(null=True, default=0)
    dislike = models.IntegerField(null=True, default=0)
    comment = models.IntegerField(null=True, default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        managed = True
        db_table = 'Question'

    objects = models.Manager()
    questManager = ManagerQuestion()

    def countRating(self):
        rating_like = weightParam['like'] * self.like
        rating_dislike = weightParam['dislike'] * self.dislike
        rating_comment = weightParam['comment'] * self.comment
        self.rating = rating_like + rating_dislike + rating_comment


class ManagerAnswer(models.Manager):
    def getNewestAnswers(self):
        return self.order_by('-date_create')

    def getPopularAnswers(self):
        return self.order_by('-rating')

    def getAnswersByQuestId(self, question_id):
        return self.filter(question=question_id).order_by('date_create')


# Нужно добавить в модель систему рейтинга
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, default=0)
    like = models.IntegerField(null=True, default=0)
    dislike = models.IntegerField(null=True, default=0)

    class Meta:
        managed = True
        db_table = 'Answer'

    objects = models.Manager()
    ansManager = ManagerAnswer()

    def countRating(self):
        self.rating = weightParam['like'] * self.like + weightParam['dislike'] * self.dislike


class AbstractReactionQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        managed = False
        abstract = True


class AbstractReactionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        managed = False
        abstract = True


# Ниже приведенные таблицы нужны исключительно для того, чтобы понимать, делать пользователь отметку на посте,
# комментарии или нет
class LikeQuestion(AbstractReactionQuestion):
    class Meta:
        managed = True
        db_table = 'LikeQuestion'
        unique_together = ["user", "question"]


class LikeAnswer(AbstractReactionAnswer):
    class Meta:
        managed = True
        db_table = 'LikeAnswer'
        unique_together = ["user", "answer"]


class DislikeQuestion(AbstractReactionQuestion):
    class Meta:
        managed = True
        db_table = 'DislikeQuestion'
        unique_together = ["user", "question"]


class DislikeAnswer(AbstractReactionAnswer):
    class Meta:
        managed = True
        db_table = 'DislikeAnswer'
        unique_together = ["user", "answer"]


# # Эти таблицы нужны для выборки лучших пользователей и тегов. Особенность в том, что их значение будет меняться только
# # через cron-скрипты
#
# class BestUsers(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     class Meta:
#         managed = True
#         db_table = 'BestUsers'
#
#
# class PopularTags(models.Model):
#     tag = models.OneToOneField(Tag, on_delete=models.CASCADE)
#
#     class Meta:
#         managed = True
#         db_table = "PopularTags"
