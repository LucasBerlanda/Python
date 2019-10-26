import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Classe onde possui as configurações da aplicação
class Config(object):

    # chave de segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'essa-e-chave-secreta'

    # configuração de conexão com o banco de dados
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/tcc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    # configuração de linhas por páginas nas listas
    POSTS_PER_PAGE = 2

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['luizberlanda05@gmail.com']

