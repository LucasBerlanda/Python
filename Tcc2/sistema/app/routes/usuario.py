from flask import render_template, url_for, redirect, request, flash  
from app import app, db
from app.models import Usuario, PerfilAcesso, Setor
from app.forms import RegistraUsuarioForm
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/cadastroUsuario', methods=['GET', 'POST'])
def cadastroUsuario():

    # renderiza o formulário na tela
    form = RegistraUsuarioForm()

    # passo a lista para o campo de selct no formulário
    form.setor.choices = [(0, "--Selecione--")]+[(setor.id, setor.nomeSetor) for setor in Setor.query.all()]
    form.perfilAcesso.choices = [(0, "--Selecione--")]+[(perfilAcesso.id, perfilAcesso.nomePerfil) for perfilAcesso in PerfilAcesso.query.all()]

    # verifica se o form submetido é válido
    if request.method == "POST":

        if form.validate_on_submit():

            try:

                user = Usuario(username=form.username.data, email=form.email.data, setor_id=form.setor.data, perfilAcesso_id=form.perfilAcesso.data,
                               password_hash=form.password.data)
                user.set_password(form.password.data)

                db.session.add(user)
                db.session.commit()
                flash('Parabéns, novo usuário registrado!', 'info')
                return redirect(url_for('index'))

            except Exception as e:
                print(e.args)

        flash('Não foi possível salvar!', 'error')
        return redirect(url_for('cadastroUsuario'))

    return render_template('usuario/registrar.html', title='Register', form=form)

@app.route("/listaUsuarios")
@login_required
def listaUsuarios():

    perfis = PerfilAcesso.query.all()
    setores = Setor.query.all()

    page = request.args.get('page', 1, type=int)
    usuarios = Usuario.query.order_by(Usuario.username).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('listaUsuarios', page=usuarios.next_num) \
        if usuarios.has_next else None
    prev_url = url_for('listaUsuarios', page=usuarios.prev_num) \
        if usuarios.has_prev else None
    

    return render_template("usuario/lista.html", usuarios = usuarios.items,
                                             next_url=next_url, prev_url=prev_url ,perfis=perfis, setores=setores, title='Lista de Usuários')

@app.route("/editarUsuario/<int:id>", methods=['GET', 'POST'])
@login_required
def editarUsuario(id):

        usuario = Usuario.query.filter_by(id=id).first()
        perfisAcesso = PerfilAcesso.query.all()
        setores = Setor.query.all()

        if request.method == "POST":

            username = (request.form.get("username"))
            email = (request.form.get("email"))
            setor_id = (request.form.get("setor_id"))
            perfilAcesso_id = (request.form.get("perfilAcesso_id"))


            user = Usuario.query.filter_by(username=username).first()

            if current_user.perfilAcesso_id == 1:
                #verifica se veio usuario ou não do select

                if user is None or user.id == id:

                    try:
                        usuario.username = username
                        usuario.email = email
                        usuario.setor_id = setor_id
                        usuario.perfilAcesso_id = perfilAcesso_id

                        db.session.commit()
                        db.session.close()

                        flash('Salvo com sucesso!', 'info')
                        return redirect(url_for("listaUsuarios"))

                    except Exception as e:
                        print(e.args)

                flash('Já existe usuário com esse nome!', 'error')
                return render_template("usuario/editar.html", usuario=usuario, perfisAcesso=perfisAcesso,
                                       setores=setores, title='Editar usuário')

            flash('Você não tem permissão de administrador!', 'error')
        return render_template("usuario/editar.html", usuario=usuario, perfisAcesso=perfisAcesso,
                               setores = setores, title='Editar usuário')


@app.route("/excluirUsuario/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirUsuario(id):

    usuario = Usuario.query.filter_by(id = id).first()

    if usuario.id != current_user.id and current_user.perfilAcesso_id == 1:

        try:
            db.session.delete(usuario)
            db.session.commit()

            flash('Usuário excluido com sucesso!', 'info')
            return redirect(url_for('listaUsuarios'))
        except Exception as e:
            print(e.args)

    flash('Você não tem permissão de administrador, ou não pode excluir seu usuário!', 'error')
    return redirect(url_for('listaUsuarios'))
