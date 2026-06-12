# Deep&Vodka — Sistema Web

Servidor web da plataforma Deep&Vodka, desenvolvido em **Django 5.2**. Gerencia eventos e sets musicais, expõe uma API REST consumida pelo app mobile e possui interface administrativa protegida por autenticação.

---

## Stack

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.13 | Linguagem base |
| Django | 5.2 | Framework web (MTV) |
| Django REST Framework | 3.x | API JSON |
| SQLite | — | Banco de dados |
| django-cors-headers | — | Libera CORS para o app mobile |

---

## Padrão MTV

O Django organiza o código em três camadas:

```
Requisição HTTP
      ↓
   urls.py          ← mapeia URL → View
      ↓
   views.py         ← processa a lógica, consulta o Model
      ↓
   models.py        ← representa e acessa o banco de dados
      ↓
  templates/        ← renderiza o HTML final
      ↓
Resposta HTTP
```

---

## Estrutura de arquivos

```
sistema/
├── sistema/
│   ├── settings.py       # configurações globais
│   └── urls.py           # roteamento principal
├── veiculos/             # app principal (eventos e sets)
│   ├── models.py         # modelos Evento e SetMusical
│   ├── views.py          # views HTML e endpoints API
│   ├── forms.py          # formulários Django
│   ├── serializers.py    # serialização JSON (DRF)
│   ├── urls.py           # rotas do app
│   ├── admin.py          # painel administrativo
│   └── tests.py          # testes unitários
├── login/
│   └── views.py          # login, logout, cadastro, LoginAPI, CadastroAPI
├── templates/
│   ├── base.html         # layout base com navbar e footer
│   ├── login.html        # página de login (standalone)
│   ├── cadastro.html     # página de cadastro (standalone)
│   ├── sobre.html        # página Sobre Nós
│   ├── evento/           # templates de eventos
│   └── set/              # templates de sets
└── static/
    └── css/app.css       # estilos globais (variáveis DVK, cards, botões)
```

---

## Models

### `Evento`
```
nome          CharField
data          DateField
hora          TimeField
local         CharField
descricao     TextField (opcional)
capacidade    IntegerField (opcional)
banner        ImageField  (opcional, salvo em media/eventos/banners/)
link_ingresso URLField    (opcional)
```
Ordenação padrão: `['data', 'hora']`

### `SetMusical`
```
nome      CharField
url       URLField
tipo      CharField — choices: 'youtube' | 'soundcloud'
descricao TextField (opcional)
data      DateField (opcional)
```
Ordenação padrão: `['-data', 'nome']`

---

## Views de interface (HTML)

Todas usam Class-Based Views do Django.

| URL | View | Acesso | Descrição |
|---|---|---|---|
| `/eventos/` | `ListarEventos` | Público | Lista todos os eventos |
| `/eventos/<id>/` | `DetalheEvento` | Público | Detalhe de um evento |
| `/eventos/novo/` | `CriarEvento` | Staff | Formulário de criação |
| `/eventos/<id>/editar/` | `EditarEvento` | Staff | Formulário de edição |
| `/eventos/<id>/excluir/` | `ExcluirEvento` | Staff | Confirmação de exclusão |
| `/eventos/banner/<arquivo>` | `BannerEvento` | Público | Serve o arquivo de imagem do banner com validação de path traversal |
| `/eventos/sets/` | `ListarSets` | Público | Lista todos os sets |
| `/eventos/sets/novo/` | `CriarSet` | Staff | Formulário de criação de set |
| `/eventos/sets/excluir/<id>/` | `ExcluirSet` | Staff | Confirmação de exclusão de set |

`LoginRequiredMixin` protege todas as views de escrita. Tentativas sem sessão ativa redirecionam para `/login/`.

---

## API REST

Base URL: `http://127.0.0.1:8000`

### Autenticação

A API aceita dois métodos:
- **Token** — `Authorization: Token <token>` (usado pelo app mobile)
- **Session** — cookie de sessão (usado pelo navegador após login)

### Endpoints

#### Eventos

| Método | URL | Autenticação | Resposta |
|---|---|---|---|
| GET | `/eventos/api/` | Nenhuma | Lista todos os eventos (JSON) |
| GET | `/eventos/api/<id>/` | Nenhuma | Detalhe de um evento |
| PUT / PATCH | `/eventos/api/<id>/` | Token obrigatório | Atualiza evento |
| DELETE | `/eventos/api/<id>/` | Token obrigatório | Remove evento (204) |

#### Sets

| Método | URL | Autenticação | Resposta |
|---|---|---|---|
| GET | `/eventos/sets/api/` | Nenhuma | Lista todos os sets (JSON) |
| GET | `/eventos/sets/api/<id>/` | Nenhuma | Detalhe de um set |
| PUT / PATCH | `/eventos/sets/api/<id>/` | Token obrigatório | Atualiza set |
| DELETE | `/eventos/sets/api/<id>/` | Token obrigatório | Remove set (204) |

#### Autenticação

| Método | URL | Body | Resposta |
|---|---|---|---|
| POST | `/autenticacao-api/` | `{username, password}` | `{id, token, is_staff, nome, email}` |
| POST | `/cadastro-api/` | `{username, password, email}` | `{id, username, token, is_staff}` |

### Exemplo de resposta — GET `/eventos/api/`
```json
[
  {
    "id": 1,
    "nome": "Deep&Vodka Open Air",
    "data": "2026-08-15",
    "hora": "20:00:00",
    "local": "Parque Cimba, Araguaína – TO",
    "descricao": "Edição especial ao ar livre.",
    "capacidade": 800,
    "banner": "/media/eventos/banners/openair.jpg",
    "link_ingresso": "https://..."
  }
]
```

---

## Autenticação e Controle de Acesso

### Usuários

Dois perfis existem no sistema:

| Perfil | `is_staff` | Pode fazer |
|---|---|---|
| Admin | `True` | Criar, editar, excluir eventos e sets; acessar `/admin/` |
| Visitante | `False` | Ver listagem e detalhes |

### Validação de senha

Aplicada em cadastro web (`CadastroView`) e cadastro via API (`CadastroAPI`):
- Mínimo de 8 caracteres
- Pelo menos um caractere especial (`!@#$%^&*` etc.)

---

## Testes Unitários

Arquivo: `veiculos/tests.py`  
Comando: `python manage.py test veiculos --verbosity=2`

### Classes de teste

#### `EventoModelTest` — Model
| Teste | O que verifica |
|---|---|
| `test_criacao_evento` | Campos salvos corretamente no banco |
| `test_str_evento` | `__str__` retorna `"Nome - data"` |
| `test_evento_sem_banner` | Banner começa vazio (campo opcional) |
| `test_evento_sem_link_ingresso` | Link de ingresso começa nulo |
| `test_ordenacao_por_data` | `Meta.ordering` ordena por data crescente |

#### `EventoViewListarTest` / `EventoViewDetalheTest` — Views públicas
| Teste | O que verifica |
|---|---|
| `test_get` | Retorna 200 com usuário autenticado |
| `test_acesso_publico` | Retorna 200 sem autenticação (página pública) |

#### `EventoViewCriarTest` / `EventoViewEditarTest` / `EventoViewExcluirTest` — Views protegidas
| Teste | O que verifica |
|---|---|
| `test_get` | Formulário abre corretamente (200) |
| `test_post` | Submissão redireciona para listagem (302) e persiste no banco |

#### `EventoAPITest` — API REST
| Teste | O que verifica |
|---|---|
| `test_api_listar_eventos` | GET retorna 200 e lista com 1 item |
| `test_api_acesso_publico` | GET sem token retorna 200 (AllowAny) |
| `test_api_detalhe_evento` | GET por ID retorna os dados corretos |
| `test_api_atualizar_evento` | PATCH com token atualiza o nome |
| `test_api_deletar_evento` | DELETE com token remove e retorna 204 |

Total: **20 testes — todos passando.**

---

## Como rodar

```bash
cd sistema/sistema
python manage.py migrate
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`
