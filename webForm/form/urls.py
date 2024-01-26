from django.urls import path

from .views import *

urlpatterns = [
    path('form/', webFormView.as_view()),
    path('home/', home, name='home'),
    ]
