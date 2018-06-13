import os
from configurations import Configuration
from .secrets import DB_USER, DB_PASSWORD, SECRET_KEY


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = SECRET_KEY

    ALLOWED_HOSTS = ['hasker.alexyvassili.me', '192.168.0.138', '127.0.0.1', 'hasker.staging.me', 'www.hasker.staging.me']


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.postgres',
        'debug_toolbar',
        'rest_framework',
        'questions',
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'hasker.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),],
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

    WSGI_APPLICATION = 'hasker.wsgi.application'


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'hasker_db',
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


    # Internationalization
    # https://docs.djangoproject.com/en/2.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
      os.path.join(BASE_DIR, "static", "static_dev"),
    )

    STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_prod")

    # Redirect to home URL after login (Default redirects to /accounts/profile/)
    LOGIN_REDIRECT_URL = '/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 20
    }


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    INTERNAL_IPS = ['127.0.0.1', ]  # For Django Debug Toolbar

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #         'LOCATION': 'questions_cache',
    #     }
    # }


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'questions_cache',
        }
    }


