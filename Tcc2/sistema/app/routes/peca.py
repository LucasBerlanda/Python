from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, NomePecas
from app.forms import RegistraPecaForm, Pesquisa
from flask_login import login_required

@app.route('/cadastroPeca', methods=['GET', 'POST'])
@login_required
def cadastroPeca():
    
    form = RegistraPecaForm()
    form.nome.choices = [(0, " Selecione ")]+[(nomePeca.id, nomePeca.nome) for nomePeca in NomePecas.query.all()]

    if form.validate_on_submit():

        nomePeca = dict(form.nome.choices).get(form.nome.data)
        descricao = form.descricao.data

        descricaoPeca = Peca.query.filter_by(descricao=descricao).first()

        if descricaoPeca is None:

            try:

                peca = Peca(nome=nomePeca, descricao=descricao)

                db.session.add(peca)
                db.session.commit()

                flash('Peça Cadastrada com sucesso!', 'info')
                return redirect(url_for('index'))

            except Exception as e:

                print(e.args)

        flash('Já existe peça cadastrada com essa descrição!', 'error')
    return render_template('peca/cadastro.html', form=form, title='Cadastro de peça')
    
@app.route("/listaPecas")
@login_required
def listaPecas():

    page = request.args.get('page', 1, type=int)
    pecas = Peca.query.order_by(Peca.nome).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('listaPecas', page=pecas.next_num) \
        if pecas.has_next else None
    prev_url = url_for('listaPecas', page=pecas.prev_num) \
        if pecas.has_prev else None

    return render_template("peca/lista.html", pecas=pecas.items, next_url=next_url, prev_url=prev_url, title='Lista de peça')


@app.route("/editarPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def editarPeca(id):

    peca = Peca.query.filter_by(id = id).first()
    
    if request.method == "POST":

        nome = (request.form.get("nome"))
        descricao = (request.form.get("descricao"))
        qtEstoque = (request.form.get("qtEstoque"))

        if nome and descricao and qtEstoque:

            descricaoPeca = Peca.query.filter_by(descricao=descricao).first()

            if descricaoPeca is None or descricaoPeca.id == id:
                try:
                    peca.nomePeca = nome
                    peca.descricao = descricao
                    peca.qtEstoque = qtEstoque

                    db.session.commit()

                    flash('Salvo com sucesso!', 'info')
                    return redirect(url_for("listaPecas"))

                except Exception as e:

                    print(e.args)

        flash('Já possui peça cadastrada com essa descrição!', 'error')
    return render_template("peca/editar.html", peca=peca, title='Editar peça')

@app.route("/excluirPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirpeca(id):

    peca = Peca.query.filter_by(id = id).first()
    # verifico se possui alguma bomba_peca vinculada a essa peca
    bomba_peca = Bomba_peca.query.filter_by(peca_id = id).first()

    # se bomba peça for none eu excluo pois não possui vinculos com bombas
    if not bomba_peca or bomba_peca is None:
        try:

            db.session.delete(peca)
            db.session.commit()

            flash("Peca excluida com sucesso!", 'info')
            return redirect(url_for('listaPecas'))

        except Exception as e:
            print(e.args)

    flash("Não é possível excluir pois possui vínculos com bombas!", 'error')
    return redirect(url_for('listaPecas'))


# @app.route("/buscaPecaDescricao")
# @login_required
# def buscaPecaDescricao(descricao):
#
#     page = request.args.get('page', 1, type=int)
#     pecas = Peca.query.filter_by(descricao=descricao).order_by(Peca.nome).paginate(page, app.config['POSTS_PER_PAGE'], False)
#
#     next_url = url_for('listaPecas', page=pecas.next_num) \
#         if pecas.has_next else None
#     prev_url = url_for('listaPecas', page=pecas.prev_num) \
#         if pecas.has_prev else None
#
#     return render_template("peca/lista.html", pecas=pecas.items, next_url=next_url, prev_url=prev_url, title='Lista de peça')
