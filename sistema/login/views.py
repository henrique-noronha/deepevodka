from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import re

ESPECIAIS = re.compile(r'[!@#$%^&*(),.?":{}|<>_\-+=\\/\[\]~]')

def validar_senha(password):
    if len(password) < 8:
        return 'A senha deve ter pelo menos 8 caracteres.'
    if not ESPECIAIS.search(password):
        return 'A senha deve conter pelo menos um caractere especial (!@#$%^&* etc).'
    return None

class login_view(View):

    def get(self, request):
        Contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect("/eventos/")
        else:
            return render(request, 'login.html', Contexto)
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/eventos/")
            
            return render( request, 'login.html',  {'mensagem': 'Usuário inativo'})
        
        return render( request, 'login.html',  {'mensagem': 'Usuário ou senha inválidos'})
    
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    
    

class CadastroView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/eventos/')
        return render(request, 'cadastro.html', {'mensagem': ''})

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirmar = request.POST.get('confirmar', '').strip()
        email = request.POST.get('email', '').strip()

        if not username or not password:
            return render(request, 'cadastro.html', {'mensagem': 'Usuário e senha são obrigatórios.'})

        erro_senha = validar_senha(password)
        if erro_senha:
            return render(request, 'cadastro.html', {'mensagem': erro_senha})

        if password != confirmar:
            return render(request, 'cadastro.html', {'mensagem': 'As senhas não coincidem.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'mensagem': 'Nome de usuário já está em uso.'})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('/eventos/')


class CadastroAPI(APIView):

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        email = request.data.get('email', '').strip()

        if not username or not password:
            return Response({'erro': 'Usuário e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        erro_senha = validar_senha(password)
        if erro_senha:
            return Response({'erro': erro_senha}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'erro': 'Nome de usuário já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'id': user.id,
            'username': user.username,
            'token': token.key,
            'is_staff': user.is_staff
        }, status=status.HTTP_201_CREATED)


class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key,
            'is_staff': user.is_staff
        })
    
