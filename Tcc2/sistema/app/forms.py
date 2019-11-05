from builtins import min

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms.widgets.html5 import NumberInput
from app.models import Usuario, TipoBomba, Peca, Setor

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired("Por favor, preencha o campo.")])
    password = PasswordField('Senha', validators=[DataRequired("Por favor, preencha o campo.")])
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
    tipo =  StringField('Tipo/Modelo:', validators=[DataRequired("Por favor, preencha o campo.")])
    mca = FloatField('Mca:', validators=[DataRequired("Por favor, preencha o campo.")])
    rotacao = IntegerField('Rotação:', validators=[DataRequired("Por favor, preencha o campo.")])
    rolamento = SelectField('Rolamentos:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    retentorDianteiro = SelectField('Retentor Dianteiro:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    retentorTraseiro = SelectField('Retentor Traseiro:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    tampaDianteira = SelectField('Tampa Dianteira:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    tampaTraseira = SelectField('Tampa Traseira:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    placa = SelectField('Placa:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    eixo = SelectField('Eixo:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    rotor = SelectField('Rotor:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    bucha = SelectField('Bucha:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    submit = SubmitField('Salvar')
    
class RegistraPecaForm(FlaskForm):
    nome = SelectField('Nome Peça:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[], coerce=int)
    descricao = StringField('Descrição:', validators=[DataRequired("Por favor, preencha o campo.")])
    submit = SubmitField('Salvar')

class RegistraSetorForm(FlaskForm):
    nomeSetor = StringField('Nome Setor:', validators=[DataRequired("Por favor, preencha o campo.")])
    abreviatura = StringField('Abreviatura:', validators=[DataRequired("Por favor, preencha o campo.")])
    descricao = StringField('Descrição:', validators=[DataRequired("Por favor, preencha o campo.")])
    submit = SubmitField('Salvar')

    def validate_setor(self, nomeSetor):
        setor = Setor.query.filter_by(nomeSetor=nomeSetor.data).first()
        if setor is not None:
            return False
    
class BuscaBombasIntercambiaveis_byTipo(FlaskForm):
    buscaEquipamentos = StringField('Busca:', validators=[DataRequired("Por favor, preencha o campo.")])

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Por favor, preencha o campo."), Email("Digite um email válido!")])
    submit = SubmitField('Enviar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha:', validators=[DataRequired("Por favor, preencha o campo.")])
    password2 = PasswordField(
        'Confirmação de Senha:', validators=[DataRequired("Por favor, preencha o campo."), EqualTo('password')])

class Pesquisa(FlaskForm):
    pesquisa = StringField('Buscar:', validators=[DataRequired("Por favor, preencha o campo.")])

class RequisicaoForm(FlaskForm):
    tipoEquipamento = SelectField('Tipo:', validators=[DataRequired("Por favor, preencha o campo.")], choices=[(0,'Selecione'), (1,'Bomba'), (2,'Peça')], coerce=int)
    bomba = StringField('Bomba:')
    peca = StringField('Peça:')
    quantidade = IntegerField('Quantidade:', validators=[DataRequired("Por favor, preencha o campo."), Length(min=1, max=100)], widget=NumberInput())
    observacao = StringField('Observação:', validators=[Length(max=50)])
