# Arquivo: clientes/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cliente
from django.db.models import Q # Essencial para buscas complexas (OU)

@login_required # Garante que apenas usuários logados acessem esta página
def lista_clientes(request):
    # Pega o valor do campo de busca (name="q") da URL, se existir
    query = request.GET.get('q')

    if query:
        # Se houver uma busca, filtra os clientes.
        # O '__icontains' faz uma busca "case-insensitive" (não diferencia maiúsculas/minúsculas).
        # O 'Q' permite combinar buscas com um "OU" lógico.
        clientes = Cliente.objects.filter(
            Q(usuario__nome_completo__icontains=query) | 
            Q(cpf__icontains=query)
        ).order_by('usuario__nome_completo') # Ordena por nome
    else:
        # Se não houver busca, pega todos os clientes
        clientes = Cliente.objects.all().order_by('usuario__nome_completo') # Ordena por nome

    # 'context' é um dicionário que envia os dados para o template
    context = {
        'clientes': clientes,
        'query': query, # Envia o termo de busca de volta para o template
    }
    return render(request, 'clientes/lista_clientes.html', context)