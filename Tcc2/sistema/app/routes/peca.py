from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, NomePecas
from app.forms import RegistraPecaForm
from flask_login import login_required

@app.route('/cadastroPeca', methods=['GET', 'POST'])
@login_required
def cadastroPeca():
    
    form = RegistraPecaForm()
    lista = [(nomePeca.id, nomePeca.nome) for nomePeca in NomePecas.query.all()]
    #lista.append((1, "Selecione"))
    form.nome.choices = lista

    if form.validate_on_submit():
        nomePeca = dict(form.nome.choices).get(form.nome.data)
        descricao = form.descricao.data

        descricaoPecas = Peca.query.filter_by(descricao = descricao).first()

        #if not descricaoPecas or descricaoPecas is None:
        peca = Peca(nome=nomePeca, descricao=descricao)
        db.session.add(peca)
        db.session.commit()
        flash('Peça Cadastrada com sucesso!', 'info')
        return redirect(url_for('index'))
        #flash('Já existe peça cadastrada com essa descrição!', 'error')
    return render_template('peca/cadastro.html', form=form, icone="fas fa-plus", bloco1="Cadastro", bloco2="Peça")
    
@app.route("/listaPecas")
@login_required
def listaPecas():

    page = request.args.get('page', 1, type=int)
    pecas = Peca.query.order_by(Peca.nome).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('listaPecas', page=pecas.next_num) \
        if pecas.has_next else None
    prev_url = url_for('listaPecas', page=pecas.prev_num) \
        if pecas.has_prev else None

    return render_template("peca/lista.html", pecas = pecas.items, next_url=next_url, prev_url=prev_url ,icone="fas fa-list", bloco1="Lista", bloco2="Peças")


@app.route("/editarPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def editarPeca(id):
    peca = Peca.query.filter_by(id = id).first()
    
    if request.method == "POST":
        nome = (request.form.get("nome"))
        descricao = (request.form.get("descricao"))

        if nome and descricao:
            descricaoPeca = Peca.query.filter_by(descricao=descricao).first()

            if not descricaoPeca or descricaoPeca is None or descricaoPeca.id == id:
                peca.nomePeca = nome
                peca.descricao = descricao

                db.session.commit()

                flash('Salvo com sucesso!', 'info')
                return redirect(url_for("listaPecas"))

        flash('Já possui peça cadastrada com essa descrição!', 'error')
    return render_template("peca/editar.html", peca=peca, icone="fas fa-pen", bloco1="Edição", bloco2="Peça")

@app.route("/excluirPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirpeca(id):
    peca = Peca.query.filter_by(id = id).first()
    bomba_peca = Bomba_peca.query.filter_by(peca_id = id).first()
    
    if not bomba_peca or bomba_peca is None:
        
        db.session.delete(peca)
        db.session.commit()
        
        flash("Peca excluida com sucesso!", 'info')
        return redirect(url_for('listaPecas'))
    
    flash("Não é possível excluir pois possui vínculos com bombas!", 'error')
    return redirect(url_for('listaPecas'))