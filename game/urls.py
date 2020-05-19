from django.urls import path
from . import views

urlpatterns = [
    path('', views.play, name='play'),
    path('results/', views.results, name='results'),
    path('scores/', views.scores, name='scores'),
]
