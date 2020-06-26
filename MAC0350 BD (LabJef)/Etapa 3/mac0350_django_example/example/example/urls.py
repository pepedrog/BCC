from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query_usuario', views.query_usuario, name='query_usuario'),
    path('query_servico', views.query_servico, name='query_servico'),
    path('query_perfil', views.query_perfil, name='query_perfil'),
    path('query_exame', views.query_exame, name='query_exame'),
    path('query_especial', views.query_especial, name='query_especial')
]
