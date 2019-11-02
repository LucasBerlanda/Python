from builtins import min

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import Usuario, TipoBomba, Peca, Setor
from wtforms.widgets import html5


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembre Me')

class RegistraUsuarioForm(FlaskForm):
    # campo tipo texto
    username = StringField('Usuário:', validators=[DataRequired("Por favor, preencha o campo.")])
    # campo tipo texto com validação de Email
    email = StringField('Email:', validators=[DataRequired("Por favor, ensira um endereço de email!"), Email("Digite um email válido!")])
    # campo tipo Password
    password = PasswordField('Senha:', validators=[DataRequired("Por favor, preencha o campo.")])
    password2 = PasswordField(
        'Confirmação de Senha:', validators=[DataRequired("Por favor, preencha o campo."), EqualTo('password')])
    setor = SelectField('Setor:', choices=[], coerce=int)
    # campo tipo select, onde em seus parâmetros é passado um Choices(lista)
    perfilAcesso = SelectField('Perfil de Acesso:', choices=[], coerce=int)

    # Método que verifica se username já existe e retorna a mensagem para a tela
    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Usuário já existente!')
    
class RegistraTipoBombaForm(FlaskForm):
    tipo =  StringField('Tipo/Modelo:', validators=[DataRequired()])
    mca = FloatField('Mca:', validators=[DataRequired()])
    rotacao = IntegerField('Rotação:', validators=[DataRequired()])
    rolamentoDianteiro = SelectField('Rolamento Dianteiro:', validators=[DataRequired()], choices=[], coerce=int)
    rolamentoTraseiro = SelectField('Rolamento Traseiro:', validators=[DataRequired()], choices=[], coerce=int)
    retentorDianteiro = SelectField('Retentor Dianteiro:', validators=[DataRequired()], choices=[], coerce=int)
    retentorTraseiro = SelectField('Retentor Traseiro:', validators=[DataRequired()], choices=[], coerce=int)
    tampaDianteira = SelectField('Tampa Dianteira:', validators=[DataRequired()], choices=[], coerce=int)
    tampaTraseira = SelectField('Tampa Traseira:', validators=[DataRequired()], choices=[], coerce=int)
    placa = SelectField('Placa:', validators=[DataRequired()], choices=[], coerce=int)
    eixo = SelectField('Eixo:', validators=[DataRequired()], choices=[], coerce=int)
    rotor = SelectField('Rotor:', validators=[DataRequired()], choices=[], coerce=int)
    bucha = SelectField('Bucha:', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField('Salvar')
    
class RegistraPecaForm(FlaskForm):
    nome = SelectField('Nome Peça:', validators=[DataRequired()], choices=[], coerce=int)
    descricao = StringField('Descrição:', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class RegistraSetorForm(FlaskForm):
    nomeSetor = StringField('Nome Setor:', validators=[DataRequired()])
    abreviatura = StringField('Abreviatura:', validators=[DataRequired()])
    descricao = StringField('Descrição:', validators=[DataRequired()]) 
    submit = SubmitField('Salvar')

    def validate_setor(self, nomeSetor):
        setor = Setor.query.filter_by(nomeSetor=nomeSetor.data).first()
        if setor is not None:
            return False
    
class BuscaBombasIntercambiaveis_byTipo(FlaskForm):
    buscaEquipamentos = StringField('Busca:', validators=[DataRequired()])

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')