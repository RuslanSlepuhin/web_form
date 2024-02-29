from django.urls import path

from .views import *

urlpatterns = [
    path('form/', webFormView.as_view()),
    path('home/', home, name='home'),
    path('a6557/', home_rus, name='home_rus'),
    path('form_is_completed/', form_is_completed, name='form_is_completed'),
    ]
