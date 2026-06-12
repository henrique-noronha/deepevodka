from django.urls import path
from .views import *

urlpatterns = [
    path('', ListarEventos.as_view(), name='listar-eventos'),
    path('<int:pk>/', DetalheEvento.as_view(), name='detalhe-evento'),
    path('banners/<str:arquivo>/', BannerEvento.as_view(), name='banner-evento'),
    path('editar/<int:pk>/', EditarEvento.as_view(), name='editar-evento'),
    path('novo/', CriarEvento.as_view(), name='criar-evento'),
    path('excluir/<int:pk>/', ExcluirEvento.as_view(), name='excluir-evento'),
    path('api/', APIListaEventos.as_view(), name='api-listar-eventos'),
    path('api/<int:pk>/', APIDeletarEvento.as_view(), name='api-detalhe-evento'),
    path('sets/', ListarSets.as_view(), name='listar-sets'),
    path('sets/novo/', CriarSet.as_view(), name='criar-set'),
    path('sets/excluir/<int:pk>/', ExcluirSet.as_view(), name='excluir-set'),
    path('sets/api/', APIListaSets.as_view(), name='api-listar-sets'),
    path('sets/api/<int:pk>/', APIDetalheSet.as_view(), name='api-detalhe-set'),
]
