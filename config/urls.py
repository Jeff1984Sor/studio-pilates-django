# Arquivo: config/urls.py

from django.contrib import admin
from django.urls import path

# Importações necessárias para as views de autenticação e redirecionamento
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

# Importação das nossas views customizadas do app 'accounts'
from accounts import views as accounts_views


# Este é o "mapa de rotas" principal do seu site.
# O Django lê esta lista de cima para baixo.
urlpatterns = [
    # Rota 1: Redireciona a página inicial (caminho vazio) para a página de login.
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),

    # Rota 2: A página de administração padrão do Django.
    path('admin/', admin.site.urls),

    # Rota 3: Nossa página de login personalizada.
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Rota 4: A funcionalidade de logout, que redireciona para o login após sair.
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rota 5: Nosso dashboard, que só pode ser acessado por usuários logados.
    path('dashboard/', accounts_views.dashboard, name='dashboard'),
]