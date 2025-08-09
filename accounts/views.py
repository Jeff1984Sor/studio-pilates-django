from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# O decorator @login_required garante que só usuários logados podem ver esta página.
# Se um usuário não logado tentar acessar, ele será automaticamente redirecionado 
# para a página de login que definimos no settings.py (LOGIN_URL).
@login_required
def dashboard(request):
    # Por enquanto, esta view apenas renderiza um template HTML.
    # No futuro, podemos passar informações extras para o template aqui.
    return render(request, 'accounts/dashboard.html')