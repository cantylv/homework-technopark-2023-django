from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.urls import reverse
from . import views

urlpatterns = [
    path('', views.listing, name='home'),  # questions
    path('about/', views.about, name='about'),  # about me
    path('tag/<str:tag_name>/', views.tag, name='tag'),  # tagged questions
    path('question/<int:question_id>/', views.question, name='question'),  # question and answers
    # если такого пользователя не существует, делаем редирект на главную страницу или на нашего юзера
    path('user/profile/<str:username>/', views.profile, name='profile'),  # user profile
    path('user/auth/', views.authorization, name='auth'),  # login
    path('user/reg/', views.registration, name='reg'),  # registration
    path('user/logout', views.user_logout, name='logout'),
    path('user/ask/', views.ask, name='ask'),  # ask question

    path('changeReaction/', views.changeReaction, name='reaction'),
    path('rightAnswer/', views.rightAnswer, name='isRightAnswer'),

    # общий путь для перенаправлений на соответствующие страницы с помощью рег выражений
    re_path(r'^about(/.*)?$', RedirectView.as_view(url='/about/')),
    re_path(r'^tag/(?P<tag_name>[\w-]+)/.*$', RedirectView.as_view(pattern_name='tag')),
    re_path(r'^question/(?P<question_id>\d+)/.*$', RedirectView.as_view(pattern_name='question')),
    re_path(r'^user/profile/(?P<username>[\w-]+)/.*$', RedirectView.as_view(pattern_name='profile')),
    re_path(r'^user/auth/.*', RedirectView.as_view(url='/user/auth/')),
    re_path(r'^user/reg/.*', RedirectView.as_view(url='/user/reg/')),
    re_path(r'^user/ask(/.*)?$', RedirectView.as_view(url="/user/ask/")),
    re_path(r'^(?!uploads/+|static/+|admin/+).*$', RedirectView.as_view(url="/"))
]
