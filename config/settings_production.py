"""
Production settings for PythonAnywhere deployment
"""

from .settings import *

# SECURITY: Turn off debug mode in production
DEBUG = False

# Your PythonAnywhere domain
ALLOWED_HOSTS = ['whitesong.pythonanywhere.com']

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/whitesong/StemCellResourceBank_v0/staticfiles'

# Media files configuration for PythonAnywhere
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/whitesong/StemCellResourceBank_v0/media'

# Optional: Generate a new secret key for production
# You can generate one at: https://djecrety.ir/
# SECRET_KEY = 'your-new-secret-key-here'

