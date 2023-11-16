from django.shortcuts import render
from django.http import HttpResponse


def listing(req):
    return render(req, 'app/public/listing.html', {
        'data': {
            'user_token': 'XX'
        }
    })


def question(req):
    return render(req, 'app/public/question.html', {
        'data': {
            'user_token': 'XXX'
        }
    })


def profile(req):
    return render(req, 'app/public/profile.html')


def tag(req):
    return render(req, 'app/public/tag_question.html')


def authorization(req):
    return render(req, 'app/public/authorization.html')


def registration(req):
    return render(req, 'app/public/registration.html')


def ask(req):
    return render(req, 'app/public/ask.html', {
        'data': {
            'user_token': 'XXX'
        }
    })


def about(req):
    return render(req, 'app/public/base.html')  # need to make layout for page layout