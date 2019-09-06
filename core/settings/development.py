from core.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite3.db',
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': os.environ.get('DB_NAME', 'sistemagcm'),
        #'USER': os.environ.get('DB_USER', 'admin_gcm'),
        #'PASSWORD': os.environ.get('DB_PASS', 'gcmapiai'),
        #'HOST': '127.0.0.1',
        #'PORT': '5432'
    }
}
