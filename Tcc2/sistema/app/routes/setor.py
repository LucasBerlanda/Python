from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import Setor, Usuario
from app.forms import RegistraSetorForm
from flask_login import login_required


@app.route('/cadastroSetor', methods=['GET', 'POST'])
@login_required
def cadastroSetor():
   
    form = RegistraSetorForm()
    if form.validate_on_submit():
        nomeSetor = form.nomeSetor.data

        existeSetor = Setor.query.filter_by(nomeSetor=nomeSetor).first()

        if not existeSetor or excluirSetor is None:
            try:

                setor = Setor(nomeSetor=nomeSetor, descricao=form.descricao.data, abreviatura=form.abreviatura.data)
                db.session.add(setor)
                db.session.commit()
                flash('Setor Cadastrado com sucesso!', 'info')
                return redirect(url_for('index'))

            except Exception as e:
                print(e.args)

        flash('Já possui esse setor cadastrado!', 'error')
    return render_template('setor/cadastro.html', form=form, icone="fas fa-plus", bloco1="Cadastro", bloco2="Setor")

@app.route("/listaSetores")
@login_required
def listaSetores():

    page = request.args.get('page', 1, type=int)
    setores = Setor.query.order_by(Setor.nomeSetor).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('listaSetores', page=setores.next_num) \
        if setores.has_next else None
    prev_url = url_for('listaSetores', page=setores.prev_num) \
        if setores.has_prev else None
    
    return render_template("setor/lista.html", setores=setores.items, next_url=next_url, prev_url=prev_url ,icone="fas fa-list", bloco1="Lista", bloco2="Setores")


@app.route("/editarSetor/<int:id>", methods=['GET', 'POST'])
@login_required
def editarSetor(id):

    setor = Setor.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        nomeSetor = (request.form.get("nomeSetor"))
        abreviatura = (request.form.get("abreviatura"))
        descricao = (request.form.get("descricao"))

        if nomeSetor and abreviatura and descricao:

            existeSetor = Setor.query.filter_by(nomeSetor=nomeSetor).first()

            # verifica se veio usuario ou não do select
            if not existeSetor or existeSetor is None or existeSetor.id == id:

                try:
                    setor.nomeSetor = nomeSetor
                    setor.abreviatura = abreviatura
                    setor.descricao = descricao

                    db.session.commit()

                    flash('Salvo com sucesso!', 'info')
                    return redirect(url_for("listaSetores"))

                except Exception as e:
                    print(e.args)

        flash('Já possui esse setor cadastrado!', 'error')
    return render_template("setor/editar.html", setor=setor, icone="fas fa-pen", bloco1="Edição", bloco2="Setor")

@app.route("/excluirSetor/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirSetor(id):

    setor = Setor.query.filter_by(id=id).first()
    user = Usuario.query.filter_by(setor_id=id).first()
    
    if not user or user is None:

        try:
            db.session.delete(setor)
            db.session.commit()

            flash("Setor excluido com sucesso!", 'info')
            return redirect(url_for('listaSetores'))

        except Exception as e:
            print(e.args)

    flash("Não é possível excluir pois possui vínculos com usuários!", 'error')
    return redirect(url_for('listaSetores'))
    
    


