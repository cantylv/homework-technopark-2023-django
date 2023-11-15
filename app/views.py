from django.shortcuts import render
from django.http import HttpResponse


def listing(req):
    questions = []
    return render(req, 'app/public/user_unauthorized/listing_unauthorized.html')


def question(req):
    return render(req, 'app/public/user_unauthorized/question_unauthorized.html')


def profile(req):
    return render(req, 'app/public/user_unauthorized/tag_questions_unauthorized.html')


def tag(req):
    return render(req, 'app/public/user_unauthorized/tag_questions_unauthorized.html')


def authorization(req):
    return render(req, 'app/public/authorization.html')


def registration(req):
    return render(req, 'app/public/registration.html')
