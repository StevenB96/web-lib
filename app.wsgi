import os
import sys

# Add the path to the Django project directory
sys.path.append('./')
sys.path.append('./venv/Lib/site-packages')

# Set the environment variable to tell Django where your settings module is located
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "livi_assessment.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()