from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing, name='home'),  # you need to do paginator and limit number of visible questions
    path('about/', views.about, name='about'),  # finished page
    path('tag/<str:tag_name>/', views.tag, name='tag'),  # tagged questions
    path('question/<int:question_id>/', views.question, name='question'),  # question and answers
    path('user/profile/<str:login>', views.profile, name='profile'),  # user profile
    path('user/auth/', views.authorization, name='auth'),  # login
    path('user/reg/', views.registration, name='reg'),  # registration
    path('user/ask/', views.ask, name='ask'),  # ask question
]
