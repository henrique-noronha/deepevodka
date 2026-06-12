"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from login.views import *
from django.conf.urls.static import static


class SobreView(TemplateView):
    template_name = 'sobre.html'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/eventos/', permanent=False)),
    path('login/', login_view.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('Logout/', Logout.as_view(), name='logout'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('eventos/', include('veiculos.urls')),
    path('autenticacao-api/', LoginAPI.as_view()),
    path('cadastro-api/', CadastroAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)