from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nfa_to_dfa', views.nfa_to_dfa, name='nfa2dfa')
]