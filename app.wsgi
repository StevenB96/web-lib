import os
import sys
from django.core.wsgi import get_wsgi_application

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Add the current directory and the virtual environment to the Python path
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'venv', 'lib', 'python3.11', 'site-packages'))

# Set the environment variable to tell Django where your settings module is located
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "livi_assessment.settings")

application = get_wsgi_application()