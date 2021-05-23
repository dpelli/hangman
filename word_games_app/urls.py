from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('word_jumble', views.word_jumble),
    path('guess', views.guess),
    path('reset', views.reset),
    path('start', views.start),
    path('logout', views.logout),
]