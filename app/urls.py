from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing, name='home'),  # listing questions
    path('home/', views.listing, name='home'),  # listing questions
    path('about/', views.about, name='about'),  # NEED TO DO
    path('hot/', views.listing, name='hot_quest'),  # hot questions       NEED TO DO
    path('news/', views.listing, name='new_quest'),  # new questions      NEED TO DO
    path('tag/django/', views.tag, name='tag_url'),  # tag questions
    path('question/35/', views.question, name='question_url'),  # question and answers
    path('user/profile/', views.profile, name='profile'),  # user profile
    path('user/auth/', views.authorization, name='auth'),  # login
    path('user/reg/', views.registration, name='reg'),  # registration
    path('user/ask/', views.ask, name='ask'),  # ask question
]
