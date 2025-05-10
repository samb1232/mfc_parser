class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/mfc_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    
    DB_NAME = 'mfc_db'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'db'
    DB_PORT = '5432'
