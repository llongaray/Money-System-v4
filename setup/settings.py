import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Definição do diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações gerais do projeto

# Chave secreta para segurança
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# Debug ativado para ambiente de desenvolvimento
DEBUG = True

# Hosts permitidos durante o desenvolvimento
ALLOWED_HOSTS = ['127.0.0.1', '192.168.18.236', '192.168.18.223']

# Definição de Aplicações
INSTALLED_APPS = [
    'django.contrib.admin',  # Aplicativo do painel de administração do Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.dashboard.apps.DashboardConfig',
    'apps.financeiro.apps.FinanceiroConfig',
    'apps.recursos_humanos.apps.RecursosHumanosConfig',
    'apps.vendas.apps.VendasConfig',
]

# Middlewares para processamento de requisições
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL principal do projeto
ROOT_URLCONF = 'setup.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '.templates'),
            os.path.join(BASE_DIR, '.templates/apps'),
            os.path.join(BASE_DIR, '.templates/partials')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do aplicativo WSGI
WSGI_APPLICATION = 'setup.wsgi.application'

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuração de validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configurações de internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static', 'img'),
    os.path.join(BASE_DIR, 'static', 'css'),
    os.path.join(BASE_DIR, 'static', 'js'),
]

# Configurações de arquivos de mídia
MEDIA_URL = '/.media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '.media')

# Tipo de campo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de opções de frame X-Frame
X_FRAME_OPTIONS = "SAMEORIGIN"
