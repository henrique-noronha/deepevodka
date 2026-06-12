from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from veiculos.models import Evento
import datetime


class EventoModelTest(TestCase):

    def setUp(self):
        self.evento = Evento.objects.create(
            nome='Show de Verão',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Clube XYZ',
            descricao='Grande festa de fim de ano.',
            capacidade=500,
        )

    def test_criacao_evento(self):
        self.assertEqual(self.evento.nome, 'Show de Verão')
        self.assertEqual(self.evento.local, 'Clube XYZ')
        self.assertEqual(self.evento.capacidade, 500)

    def test_str_evento(self):
        self.assertEqual(str(self.evento), 'Show de Verão - 2026-12-31')

    def test_evento_sem_banner(self):
        self.assertFalse(self.evento.banner)

    def test_evento_sem_link_ingresso(self):
        self.assertIsNone(self.evento.link_ingresso)

    def test_ordenacao_por_data(self):
        evento_anterior = Evento.objects.create(
            nome='Festa Anterior',
            data=datetime.date(2026, 6, 1),
            hora=datetime.time(20, 0),
            local='Bar ABC',
        )
        eventos = list(Evento.objects.all())
        self.assertEqual(eventos[0], evento_anterior)
        self.assertEqual(eventos[1], self.evento)


class EventoViewListarTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.url = reverse('listar-eventos')
        self.evento = Evento.objects.create(
            nome='Evento Teste',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Local Teste',
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('eventos')), 1)

    def test_acesso_publico(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class EventoViewDetalheTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.evento = Evento.objects.create(
            nome='Evento Detalhe',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Local Detalhe',
        )
        self.url = reverse('detalhe-evento', kwargs={'pk': self.evento.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Evento Detalhe')

    def test_acesso_publico(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class EventoViewCriarTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.url = reverse('criar-evento')
        self.form_data = {
            'nome': 'Novo Evento',
            'data': '2026-12-31',
            'hora': '22:00',
            'local': 'Algum Local',
            'descricao': '',
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-eventos'))
        self.assertEqual(Evento.objects.count(), 1)
        self.assertEqual(Evento.objects.first().nome, 'Novo Evento')


class EventoViewEditarTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.evento = Evento.objects.create(
            nome='Evento Original',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Local Original',
        )
        self.url = reverse('editar-evento', kwargs={'pk': self.evento.pk})
        self.form_data = {
            'nome': 'Evento Editado',
            'data': '2026-12-31',
            'hora': '23:00',
            'local': 'Novo Local',
            'descricao': '',
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-eventos'))
        self.evento.refresh_from_db()
        self.assertEqual(self.evento.nome, 'Evento Editado')


class EventoViewExcluirTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.evento = Evento.objects.create(
            nome='Evento para Excluir',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Local',
        )
        self.url = reverse('excluir-evento', kwargs={'pk': self.evento.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-eventos'))
        self.assertEqual(Evento.objects.count(), 0)


class EventoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(username='apiuser', password='senha123')
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.evento = Evento.objects.create(
            nome='Evento API',
            data=datetime.date(2026, 12, 31),
            hora=datetime.time(22, 0),
            local='Local API',
        )

    def test_api_listar_eventos(self):
        response = self.client.get(reverse('api-listar-eventos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_api_acesso_publico(self):
        self.client.credentials()
        response = self.client.get(reverse('api-listar-eventos'))
        self.assertEqual(response.status_code, 200)

    def test_api_detalhe_evento(self):
        response = self.client.get(reverse('api-detalhe-evento', args=[self.evento.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Evento API')

    def test_api_atualizar_evento(self):
        response = self.client.patch(
            reverse('api-detalhe-evento', args=[self.evento.id]),
            {'nome': 'Evento Atualizado'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Evento Atualizado')

    def test_api_deletar_evento(self):
        response = self.client.delete(reverse('api-detalhe-evento', args=[self.evento.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Evento.objects.count(), 0)
