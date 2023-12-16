from django.db import models


class Answers(models.Model):
    text = models.TextField(blank=True, null=True)
    date_create = models.DateField(auto_now_add=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    question = models.ForeignKey('Questions', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'answers'


class Questions(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    date_create = models.DateField(auto_now_add=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    comment = models.TextField(default=0)

    class Meta:
        managed = False
        db_table = 'questions'


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tag'


class Tagquestions(models.Model):
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tagquestions'


class Users(models.Model):
    img = models.ImageField(upload_to="users/")  # url: uploads/users/photo.png
    login = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=10)
    date_reg = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'users'
