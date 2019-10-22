import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'essa-e-chave-secreta'

    #configuração de conexão com o banco de dados
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/tcc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Degug=True

    # configuração de linhas por páginas nas listas
    POSTS_PER_PAGE = 2
