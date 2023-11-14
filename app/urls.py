from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing),
    path('user/auth', views.authorization),
    path('user/reg', views.registration),
]
