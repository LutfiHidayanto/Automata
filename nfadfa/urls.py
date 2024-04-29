from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nfa_to_dfa', views.nfa_to_dfa, name='nfa2dfa'),
    path('regex_to_enfa', views.regex_to_enfa, name='regex_to_enfa'),
    path('minimize_dfa', views.minimize_dfa, name='minimize_dfa'),
    path('test_fa', views.test_fa, name='test_fa'),
    path('test_fa/<str:name>', views.test_fa_details, name='test_fa_details'),
    path('equivalent_dfa', views.equivalent_dfa, name='equivalent_dfa')
]