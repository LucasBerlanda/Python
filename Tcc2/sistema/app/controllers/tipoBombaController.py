from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import TipoBomba, Peca, Bomba_peca
from app.forms import RegistraTipoBombaForm
from flask_login import login_required
from sqlalchemy import text

@app.route('/cadastroTipoBomba', methods=['GET', 'POST'])
@login_required
def cadastroTipoBomba():

    form = RegistraTipoBombaForm()
    form.rolamentoDianteiro.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Rolamento")]
    form.rolamentoTraseiro.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Rolamento")]
    form.retentorDianteiro.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Retentor")]
    form.retentorTraseiro.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Retentor")]
    form.tampaDianteira.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Tampa")]
    form.tampaTraseira.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Tampa")]
    form.placa.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Placa")]
    form.eixo.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Eixo")]
    form.rotor.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Rotor")]
    form.bucha.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Bucha")]
    
    if form.validate_on_submit():
        
        possuiTipobomba = TipoBomba.query.filter_by(tipo= form.tipo.data).all()
        
        if not possuiTipobomba or possuiTipobomba is None:
        
            listaPecas = [form.rolamentoDianteiro.data, form.rolamentoTraseiro.data,
                        form.retentorDianteiro.data, form.retentorTraseiro.data,
                        form.tampaDianteira.data, form.tampaTraseira.data,
                        form.placa.data, form.eixo.data, form.rotor.data, form.bucha.data]
            
            tipobomba = TipoBomba(tipo=form.tipo.data, mca=form.mca.data, rotacao=form.rotacao.data)
            db.session.add(tipobomba)
            db.session.commit()
            
            getIdBomba = tipobomba.id
            
            for lista in listaPecas:
                bb_peca = Bomba_peca(tipoBomba_id=getIdBomba, peca_id=lista)
                db.session.add(bb_peca)
                db.session.commit()   
                
            flash('Bomba cadastrada com sucesso!', 'info')
            return redirect(url_for('listaTipoBombas'))
        
        flash("Já possui este Tipo/Modelo cadastrado!", 'error')
    
    return render_template('bomba/cadastro.html', form=form)


@app.route('/listaTipoBombas')
@login_required
def listaTipoBombas():
    tipoBombas = TipoBomba.query.all()

    return render_template("bomba/lista.html", tipoBombas=tipoBombas)


@app.route("/editarTipoBomba/<int:id>", methods=['GET', 'POST'])
@login_required
def editarTipoBomba(id):
    tipoBomba = TipoBomba.query.filter_by(id = id).first()
    
    if request.method == "POST":
        tipo = (request.form.get("tipo"))
        mca = (request.form.get("mca"))
        rotacao = (request.form.get("rotacao"))
        
        if tipo and mca and rotacao:
            bomba = TipoBomba.query.filter_by(tipo=tipo).first()

            if not bomba or bomba is None or bomba.id == id:
                tipoBomba.tipo = tipo
                tipoBomba.mca = mca
                tipoBomba.rotacao = rotacao

                db.session.commit()

                flash('Salvo com sucesso!', 'info')
                return redirect(url_for("listaTipoBombas"))

            flash('Já possui este Tipo/Modelo cadastrado!', 'error')

    return render_template("bomba/editar.html", tipoBomba = tipoBomba)
