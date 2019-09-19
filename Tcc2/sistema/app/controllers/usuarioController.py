from flask import render_template, url_for, redirect, request, flash  
from app import app, db
from app.models import Usuario, PerfilAcesso, Setor
from sqlalchemy import text
from app.forms import RegistraUsuarioForm
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/cadastroUsuario', methods=['GET', 'POST'])
def cadastroUsuario():
   
    form = RegistraUsuarioForm()
    form.setor.choices = [(setor.id, setor.nomeSetor) for setor in Setor.query.all()]
    form.perfilAcesso.choices = [(perfilAcesso.id, perfilAcesso.nomePerfil) for perfilAcesso in PerfilAcesso.query.all()]
    
    if form.validate_on_submit():
        print("chegou aqui")
        user = Usuario(username=form.username.data, setor_id=form.setor.data, perfilAcesso_id=form.perfilAcesso.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, novo usuário registrado!', 'info')
        return redirect(url_for('index'))
    return render_template('usuario/registrar.html', title='Register', form=form)

@app.route("/listaUsuarios")
@login_required
def listaUsuarios():
    usuarios = Usuario.query.all()
    perfis = PerfilAcesso.query.all()
    setores = Setor.query.all()
    
    #usuarios = db.session.query(Usuario).from_statement(text("select u.id, u.nomeUsuario, u.login, setor.nome from usuario u join setor s on u.setor_id = s.id join perfilacesso p on u.perfilAcesso_id = p.id")).all()

    return render_template("usuario/lista.html", usuarios = usuarios, perfis=perfis, setores=setores)

@app.route("/editarUsuario/<int:id>", methods=['GET', 'POST'])
@login_required
def editarUsuario(id):
        usuario = Usuario.query.filter_by(id = id).first()
        perfisAcesso = PerfilAcesso.query.all()
        setores = Setor.query.all()
        
        if request.method == "POST":
            username = (request.form.get("username"))
            setor_id = (request.form.get("setor_id"))
            perfilAcesso_id = (request.form.get("perfilAcesso_id"))

            if username and setor_id and perfilAcesso_id:

                #busca usuarios com o mesmo nome
                user = Usuario.query.filter_by(username=username).first()

                #verifica se veio usuario ou não do select
                if user is None:
                    usuario.username = username
                    usuario.setor_id = setor_id
                    usuario.perfilAcesso_id = perfilAcesso_id

                    db.session.commit()
                    db.session.close()

                    flash('Salvo com sucesso!', 'info')
                    return redirect(url_for("listaUsuarios"))

                flash('Já existe usuário com esse nome!', 'error')
                #return redirect(url_for("listaUsuarios"))

        return render_template("usuario/editar.html", usuario = usuario, perfisAcesso = perfisAcesso, setores = setores)


@app.route("/excluirUsuario/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirUsuario(id):
    usuario = Usuario.query.filter_by(id = id).first()
    
    userLogado = current_user.id
    
    if usuario.id != userLogado:  
        db.session.delete(usuario)
        db.session.commit()
        
        flash('Usuário excluido com sucesso!')
        return redirect(url_for('listaUsuarios'))
    
    flash('Não foi possível deletar o usuário!')
    return redirect(url_for('listaUsuarios'))
