from django.urls import path
from . import views

urlpatterns = [
    path('/', views.listing),  # listing questions
    path('/hot/', views.question),  # hot questions
    path('/news/', views.listing),  # new questions
    path('/tag/django/', views.tag),  # tag questions
    path('/question/35/', views.question),  # question and answers
    path('/profile/', views.profile),  # user profile
    path('/login/', views.authorization),  # login
    path('/signup/', views.registration),  # registration
    path('/ask/', views.registration),  # ask question
]
