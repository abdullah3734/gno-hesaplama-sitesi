import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bu-cok-gizli-bir-sifre'
    # Burası veritabanımızın yolunu ve adını belirtir.
    # Proje klasöründe app.db adında bir dosya oluşturacak.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False