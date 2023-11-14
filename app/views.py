from django.shortcuts import render
from django.http import HttpResponse


def authorization(req):
    return render(req, 'app/public/authorization.html')


def registration(req):
    return render(req, 'app/public/registration.html')


def listing(req):
    return render(req, 'app/public/user_unauthorized/listing_unauthorized.html')


