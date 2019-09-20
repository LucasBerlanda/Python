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
    username = StringField('Usuário:', validators=[DataRequired()])
    password = PasswordField('Senha:', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirmação de Senha:', validators=[DataRequired(), EqualTo('password')])
    setor = SelectField('Setor:', choices=[], coerce=int)
    perfilAcesso = SelectField('Perfil de Acesso:', choices=[], coerce=int)

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
    quantidade = IntegerField('Quantidade', validators=[NumberRange(min=1, message='Número Inválido'), DataRequired()], widget=html5.NumberInput(), default=1 )
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

