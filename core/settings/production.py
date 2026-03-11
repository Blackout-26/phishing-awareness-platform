from .base import *

# Override base settings for production security
DEBUG = False

# This will eventually pull your live domain name from the .env file
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Future Security Hardening (We will activate these in Week 12)
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

print("🔒 RUNNING IN PRODUCTION MODE")