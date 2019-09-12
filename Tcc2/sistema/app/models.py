from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class TipoBomba(db.Model):
    __tablename__ = "tipoBomba"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(10), unique=True, nullable=False)
    mca = db.Column(db.Float)
    rotacao = db.Column(db.Integer)
    
    bomba_peca = db.relationship('Bomba_peca')
   
    def __init__(self, tipo, mca, rotacao):
        
        self.tipo = tipo
        self.mca = mca
        self.rotacao = rotacao
   
        
class Peca(db.Model):
    __tablename__ = "peca"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(95), nullable=False)
    descricao = db.Column(db.String(40), unique=True, nullable=False)
    
    bomba_peca = db.relationship('Bomba_peca')

    
    def __init__(self, nome, descricao):
        
        self.nome = nome
        self.descricao = descricao


class Bomba_peca(db.Model):
    
    __tablename__ = "bomba_peca"
    
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    tipoBomba_id = db.Column(db.Integer, db.ForeignKey('tipoBomba.id'), nullable=False)
    peca_id = db.Column(db.Integer, db.ForeignKey('peca.id'), nullable=False) 
    
    def __init__(self, tipoBomba_id, peca_id):
        
        self.tipoBomba_id = tipoBomba_id
        self.peca_id = peca_id
        

class Setor(db.Model):
    
    __tablename__ = "setor"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeSetor = db.Column(db.String(20), unique=True, nullable=False)
    abreviatura = db.Column(db.String(5), unique=True)
    descricao = db.Column(db.String(100))
    
    usuario = db.relationship("Usuario")
    
    def __init__(self, nomeSetor, abreviatura, descricao):
        
        self.nomeSetor = nomeSetor
        self.abreviatura = abreviatura
        self.descricao = descricao
        
        
class PerfilAcesso(db.Model):
    
    __tablename__ = "perfilAcesso"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomePerfil = db.Column(db.String(20))
    
    usuario = db.relationship("Usuario")
    
    def __init__(self, nomePerfil):
        
        self.nomePerfil = nomePerfil


class Usuario(UserMixin, db.Model):
    
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    perfilAcesso_id = db.Column(db.Integer, db.ForeignKey('perfilAcesso.id'), nullable=False)
    
    def __init__(self, username, password_hash, setor_id, perfilAcesso_id):
    
        self.username = username
        self.password_hash = password_hash
        self.setor_id = setor_id
        self.perfilAcesso_id = perfilAcesso_id
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    
    
class NomePecas(db.Model):
    __tablename__ = "nomePecas"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(25), nullable=False)
    
    def __init__(self, nome):
        
        self.nome = nome
     
  
    
@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))  
        
db.create_all()