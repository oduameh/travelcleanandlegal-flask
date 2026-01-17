import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask application configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'travel-clean-legal-secret-key-2025'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CKEditor
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = None
    
    # Site Settings
    SITE_NAME = 'Travel Clean & Legal'
    SITE_DESCRIPTION = 'Your Complete Guide to Relocating from Nigeria'
    SITE_URL = 'https://travelcleanandlegal.live'
    CONTACT_EMAIL = 'odulolaa@gmail.com'
    
    # Google AdSense
    ADSENSE_CLIENT_ID = 'ca-pub-9012240625310684'
