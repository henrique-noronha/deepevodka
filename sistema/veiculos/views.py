from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, View, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Evento, SetMusical
from .forms import FormularioEvento, FormularioSet
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions
from veiculos.serializers import SerializadorEvento, SerializadorSet
from sistema import settings
import os


class ListarEventos(ListView):
    model = Evento
    context_object_name = 'eventos'
    template_name = 'evento/listar.html'


class DetalheEvento(DetailView):
    model = Evento
    context_object_name = 'evento'
    template_name = 'evento/detalhe.html'


class EditarEvento(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = FormularioEvento
    template_name = 'evento/editar.html'
    success_url = reverse_lazy('listar-eventos')


class ExcluirEvento(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'evento/excluir.html'
    success_url = reverse_lazy('listar-eventos')


class CriarEvento(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = FormularioEvento
    template_name = 'evento/novo.html'
    success_url = reverse_lazy('listar-eventos')


class BannerEvento(View):

    def get(self, request, arquivo):
        try:
            arquivo = os.path.basename(arquivo)
            evento = Evento.objects.get(banner='eventos/banners/{}'.format(arquivo))

            media_root = os.path.realpath(settings.MEDIA_ROOT)
            caminho_arquivo = os.path.realpath(
                os.path.join(settings.MEDIA_ROOT, evento.banner.name)
            )

            if not caminho_arquivo.startswith(media_root + os.sep):
                raise Http404("Acesso negado")

            if not os.path.exists(caminho_arquivo):
                raise Http404("Arquivo não encontrado")

            return FileResponse(open(caminho_arquivo, 'rb'), content_type='image/jpeg')

        except Evento.DoesNotExist:
            raise Http404("Evento com esse banner não encontrado")
        except Exception as e:
            raise Http404(f"Erro ao acessar o arquivo: {str(e)}")


class APIListaEventos(ListAPIView):
    serializer_class = SerializadorEvento
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Evento.objects.all()


class APIDeletarEvento(RetrieveUpdateDestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = SerializadorEvento
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListarSets(ListView):
    model = SetMusical
    context_object_name = 'sets'
    template_name = 'set/listar.html'


class CriarSet(LoginRequiredMixin, CreateView):
    model = SetMusical
    form_class = FormularioSet
    template_name = 'set/novo.html'
    success_url = reverse_lazy('listar-sets')


class ExcluirSet(LoginRequiredMixin, DeleteView):
    model = SetMusical
    template_name = 'set/excluir.html'
    success_url = reverse_lazy('listar-sets')


class APIListaSets(ListAPIView):
    serializer_class = SerializadorSet
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SetMusical.objects.all()


class APIDetalheSet(RetrieveUpdateDestroyAPIView):
    queryset = SetMusical.objects.all()
    serializer_class = SerializadorSet
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
