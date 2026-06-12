# Deep&Vodka — Plataforma Web

Servidor web da plataforma Deep&Vodka, desenvolvido em **Django 5.2**. Gerencia eventos e sets musicais, expõe uma API REST consumida pelo app mobile e possui interface administrativa protegida por autenticação.

---

## Funcionalidades

**Público (sem login)**
- Listagem e detalhes de eventos
- Listagem de sets musicais com thumbnails automáticas (YouTube e SoundCloud)
- Página Sobre Nós com links para redes sociais

**Administrador (staff)**
- Criar, editar e excluir eventos (com banner e link de ingresso)
- Criar e excluir sets musicais

---

## Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- SQLite
- Bootstrap 4 + CSS customizado

---

## Estrutura

```
sistema/
├── veiculos/             ← app principal (eventos, sets, API)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
├── login/                ← autenticação web e API
├── templates/            ← HTML (base, eventos, sets, login)
└── static/css/app.css    ← estilos globais
```

---

## API REST

Base URL: `http://127.0.0.1:8000`

| Método | Endpoint | Auth | Descrição |
|---|---|---|---|
| GET | `/eventos/api/` | Não | Lista eventos |
| GET / PATCH / DELETE | `/eventos/api/<id>/` | Token (escrita) | Detalhe / edição / exclusão |
| GET | `/eventos/sets/api/` | Não | Lista sets |
| GET / PATCH / DELETE | `/eventos/sets/api/<id>/` | Token (escrita) | Detalhe / edição / exclusão |
| POST | `/autenticacao-api/` | Não | Login → retorna token e is_staff |
| POST | `/cadastro-api/` | Não | Cadastro → retorna token |

---

## Como rodar

```bash
cd sistema
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

Para criar um superusuário (admin):
```bash
python manage.py createsuperuser
```

---

## Documentação

- [ARQUITETURA.md](ARQUITETURA.md) — detalhamento completo: MTV, models, views, API e testes

---

## Autor

**Henrique Noronha Fernandes**  

