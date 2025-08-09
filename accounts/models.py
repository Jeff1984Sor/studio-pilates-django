# Arquivo: accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- Gerenciador do Usuário ---
# Esta classe define as regras de como criar usuários.
# O Django precisa saber como criar um usuário comum e um superusuário.
class UsuarioManager(BaseUserManager):
    
    def create_user(self, email, nome_completo, password=None, **extra_fields):
        """Cria e salva um usuário com o email e senha fornecidos."""
        if not email:
            raise ValueError('O campo de Email é obrigatório')
        
        # Normaliza o email (ex: converte o domínio para minúsculas)
        email = self.normalize_email(email)
        user = self.model(email=email, nome_completo=nome_completo, **extra_fields)
        
        # Criptografa a senha antes de salvar. NUNCA salve a senha como texto puro.
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_completo, password=None, **extra_fields):
        """Cria e salva um superusuário com poderes totais."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self.create_user(email, nome_completo, password, **extra_fields)


# --- Modelo do Perfil de Usuário ---
# Ex: "Administrador", "Instrutor", "Aluno"
class PerfilUsuario(models.Model):
    # O campo 'id' (seu 'cdPerfilUsuario') é criado automaticamente pelo Django.
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Perfil")

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuário"

    def __str__(self):
        return self.nome


# --- Nosso Modelo de Usuário Personalizado ---
# Herda de AbstractBaseUser (para ter controle total) e PermissionsMixin (para permissões do Django)
class Usuario(AbstractBaseUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome do Usuário")
    email = models.EmailField(unique=True, verbose_name="Email do Usuário")
    crefito = models.CharField(max_length=20, blank=True, null=True, help_text="Apenas para instrutores")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    
    perfil = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        verbose_name="Perfil de Acesso"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Acesso ao Admin")

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    # --- AQUI ESTÁ A CORREÇÃO ---
    # Adicionamos os campos que o PermissionsMixin espera, mas com um `related_name` único.
    # Isso resolve o conflito de nomes com o modelo de usuário padrão do Django.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set", # Nome único para o nosso usuário
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set", # Nome único para o nosso usuário
        related_query_name="usuario",
    )
    # --- FIM DA CORREÇÃO ---


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email
    nome_completo = models.CharField(max_length=255, verbose_name="Nome do Usuário")
    email = models.EmailField(unique=True, verbose_name="Email do Usuário")
    crefito = models.CharField(max_length=20, blank=True, null=True, help_text="Apenas para instrutores")
    
    # Relação com PerfilUsuario. `on_delete=models.PROTECT` impede que um perfil seja apagado se houver usuários nele.
    perfil = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        verbose_name="Perfil de Acesso"
    )
    
    # Campos obrigatórios para o Django
    is_active = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Acesso ao Admin")

    # Define o gerenciador que criamos acima como o responsável por este modelo
    objects = UsuarioManager()

    # Define que o campo de 'login' será o EMAIL
    USERNAME_FIELD = 'email'
    
    # Campos que serão pedidos ao criar um superusuário pelo comando `createsuperuser`
    REQUIRED_FIELDS = ['nome_completo']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email
    
    