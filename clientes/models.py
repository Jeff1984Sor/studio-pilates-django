# Arquivo: clientes/models.py
from django.db import models
from django.conf import settings # Para pegar nosso modelo de usuário

class Cliente(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        primary_key=True
    )

    rg = models.CharField(max_length=20, unique=True, verbose_name="RG")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    def __str__(self):
        return self.usuario.nome_completo