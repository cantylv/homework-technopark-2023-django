from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


# У нас есть готовая модель User-а (django.contrib.auth.models.User)
# Создадим модель Profile, чтобы дополнить модель User аватаркой пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/')

    class Meta:
        managed = True
        db_table = 'Profile'


class ManagerQuestion(models.Manager):
    def get_queryset(self):
        return Question.objects.select_related('user__profile')

    def getNewestQuestions(self):
        return self.order_by('-date_create')

    def getPopularQuestions(self):
        return self.order_by('-rating')

    # Нужно будет добавить проверку на уникальность строки данных.
    # Сейчас пользователь может добавить много лайков к вопросу
    def getQuestionsByTag(self, tags):  # tags - строка, содержащая теги, разделенные символом @
        tags = tags.split('@')  # получили массив тегов
        return self.filter(tagquestion__tag__name__in=tags).distinct(), tags


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    rating = models.IntegerField(null=True, default=0)

    class Meta:
        managed = True
        db_table = 'Question'

    objects = models.Manager()
    questManager = ManagerQuestion()


class ManagerAnswer(models.Manager):

    def get_queryset(self):
        return Answer.objects.all().select_related('user__profile')

    def getNewestAnswers(self):
        return self.order_by('-date_create')

    def getPopularAnswers(self):
        return self.order_by('-rating')

    def getAnswersByQuestId(self, question_id):
        return self.filter(question=question_id)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, default=0)

    class Meta:
        managed = True
        db_table = 'Answer'

    objects = models.Manager()
    ansManager = ManagerAnswer()


class Tag(models.Model):
    name = models.CharField(max_length=30)
    rating = models.IntegerField(null=True, default=0)

    class Meta:
        managed = True
        db_table = 'Tag'


class TagQuestion(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'TagQuestion'


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


class LikeQuestion(AbstractReactionQuestion):
    class Meta:
        managed = True
        db_table = 'LikeQuestion'


class LikeAnswer(AbstractReactionAnswer):
    class Meta:
        managed = True
        db_table = 'LikeAnswer'


class DislikeQuestion(AbstractReactionQuestion):
    class Meta:
        managed = True
        db_table = 'DislikeQuestion'


class DislikeAnswer(AbstractReactionAnswer):
    class Meta:
        managed = True
        db_table = 'DislikeAnswer'
