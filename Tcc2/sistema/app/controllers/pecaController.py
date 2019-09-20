from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, NomePecas
from app.forms import RegistraPecaForm
from flask_login import login_required

@app.route('/cadastroPeca', methods=['GET', 'POST'])
@login_required
def cadastroPeca():
    
    form = RegistraPecaForm()
    form.nome.choices = [(nomePeca.id, nomePeca.nome) for nomePeca in NomePecas.query.all()]
    
    if form.validate_on_submit():
        nomePeca = dict(form.nome.choices).get(form.nome.data)
        descricao = form.descricao.data
        descricaoPecas = Peca.query.filter_by(descricao = descricao).first()

        if not descricaoPecas or descricaoPecas is None:
            peca = Peca(nome=nomePeca, descricao=descricao, quantidade=form.quantidade.data)
            db.session.add(peca)
            db.session.commit()
            flash('Peça Cadastrada com sucesso!', 'info')
            return redirect(url_for('index'))
        flash('Já existe peça cadastrada com essa descrição!', 'error')
    return render_template('peca/cadastro.html', form=form)
    
@app.route("/listaPecas")
@login_required
def listaPecas():
    pecas = Peca.query.all()
    return render_template("peca/lista.html", pecas = pecas)


@app.route("/editarPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def editarPeca(id):
    peca = Peca.query.filter_by(id = id).first()
    
    if request.method == "POST":
        nome = (request.form.get("nome"))
        descricao = (request.form.get("descricao"))
        quantidade = (request.form.get("quantidade"))

        if nome and descricao and quantidade:
            descricaoPeca = Peca.query.filter_by(descricao=descricao).first()

            if not descricaoPeca or descricaoPeca is None or descricaoPeca.id == id:
                peca.nomePeca = nome
                peca.descricao = descricao
                peca.quantidade = quantidade

                db.session.commit()

                flash('Salvo com sucesso!', 'info')
                return redirect(url_for("listaPecas"))

        flash('Já possui peça cadastrada com essa descrição!', 'error')
    return render_template("peca/editar.html", peca = peca)

@app.route("/excluirPeca/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirpeca(id):
    peca= Peca.query.filter_by(id = id).first()
    bomba_peca = Bomba_peca.query.filter_by(peca_id = id).first()
    
    if not bomba_peca or bomba_peca is None:
        
        db.session.delete(peca)
        db.session.commit()
        
        flash("Peca excluida com sucesso!", 'success')
        return redirect(url_for('listaPecas'))
    
    flash("Não é possível excluir pois possui vínculos com bombas!", 'error')
    return redirect(url_for('listaPecas'))