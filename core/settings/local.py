from .base import *

# Override base settings for local development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

print("RUNNING IN LOCAL DEVELOPMENT MODE")