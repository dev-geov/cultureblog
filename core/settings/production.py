from core.settings.common import *

import dj_database_url
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
