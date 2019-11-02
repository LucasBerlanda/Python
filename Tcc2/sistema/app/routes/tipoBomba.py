from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.models import TipoBomba, Peca, Bomba_peca, OrdemServico
from app.forms import RegistraTipoBombaForm
from flask_login import login_required
from sqlalchemy import text

@app.route('/cadastroTipoBomba', methods=['GET', 'POST'])
@login_required
def cadastroTipoBomba():

    form = RegistraTipoBombaForm()
    rol = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Rolamento")]
    ret = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Retentor")]
    tamp = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Tampa")]

    form.rolamentoDianteiro.choices = rol
    form.rolamentoTraseiro.choices = rol
    form.retentorDianteiro.choices = ret
    form.retentorTraseiro.choices = ret
    form.tampaDianteira.choices = tamp
    form.tampaTraseira.choices = tamp
    form.placa.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Placa")]
    form.eixo.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Eixo")]
    form.rotor.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Rotor")]
    form.bucha.choices = [(peca.id, peca.descricao) for peca in Peca.query.filter_by(nome="Bucha")]
    
    if form.validate_on_submit():
        
        possuiTipobomba = TipoBomba.query.filter_by(tipo= form.tipo.data).all()
        
        if not possuiTipobomba or possuiTipobomba is None:

            try:
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

            except Exception as e:
                print(e.args)

        flash("Já possui este Tipo/Modelo cadastrado!", 'error')
    
    return render_template('bomba/cadastro.html', form=form, icone="fas fa-plus", bloco1="Cadastro", bloco2="Bombas")


@app.route('/listaTipoBombas')
@login_required
def listaTipoBombas():

    page = request.args.get('page', 1, type=int)

    tipoBombas = TipoBomba.query.order_by(TipoBomba.tipo).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('listaTipoBombas', page=tipoBombas.next_num) \
        if tipoBombas.has_next else None
    prev_url = url_for('listaTipoBombas', page=tipoBombas.prev_num) \
        if tipoBombas.has_prev else None

    return render_template("bomba/lista.html", tipoBombas=tipoBombas.items, next_url=next_url, prev_url=prev_url ,icone="fas fa-list", bloco1="Lista", bloco2="Bombas")


@app.route("/editarTipoBomba/<int:id>", methods=['GET', 'POST'])
@login_required
def editarTipoBomba(id):
    tipoBomba = TipoBomba.query.filter_by(id = id).first()
    
    if request.method == "POST":
        tipo = (request.form.get("tipo"))
        mca = (request.form.get("mca"))
        rotacao = (request.form.get("rotacao"))
        qtEstoque = (request.form.get("qtEstoque"))
        
        if tipo and mca and rotacao and qtEstoque:
            bomba = TipoBomba.query.filter_by(tipo=tipo).first()

            if not bomba or bomba is None or bomba.id == id:

                try:
                    tipoBomba.tipo = tipo
                    tipoBomba.mca = mca
                    tipoBomba.rotacao = rotacao
                    tipoBomba.qtEstoque = qtEstoque

                    db.session.commit()

                    flash('Salvo com sucesso!', 'info')
                    return redirect(url_for("listaTipoBombas"))

                except Exception as e:
                    print(e.args)
            flash('Já possui este Tipo/Modelo cadastrado!', 'error')

    return render_template("bomba/editar.html", tipoBomba = tipoBomba, icone="fas fa-pen", bloco1="Edição", bloco2="Bombas")


@app.route("/excluirTipoBomba/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirTipoBomba(id):
    bomba = TipoBomba.query.filter_by(id=id).first()
    bb_peca = Bomba_peca.query.filter_by(tipoBomba_id=id).all()
    ordemServico = OrdemServico.query.filter_by(equipamento=id).first()

    if bomba and ordemServico is None:
        try:
            for p in bb_peca:
                db.session.delete(p)

            db.session.delete(bomba)
            db.session.commit()

            flash("Bomba e excluida com sucesso!", 'info')
            return redirect(url_for('listaTipoBombas'))

        except Exception as e:
            print(e.args)

    flash("Não é possível excluir!", 'error')
    return redirect(url_for('listaTipoBombas'))
