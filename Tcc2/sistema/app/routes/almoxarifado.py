from flask import render_template, url_for, redirect, request, flash, Response
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca, EntradaEstoque
import json
from flask_login import login_required


@app.route('/entradaEstoque', methods=['GET', 'POST'])
@login_required
def entradaEstoque():
    pecas = Peca.query.all()
    bombas = TipoBomba.query.all()

    return render_template('almoxarifado/entradaProduto.html', icone="fas fa-warehouse", pecas=pecas, bombas=bombas,
                           bloco1='Almoxarifado', bloco2="Entrada")


@app.route('/entradaProduto', methods=['GET', 'POST'])
@login_required
def entradaProduto():

    if request.method == 'POST':

        modelo = (request.form.get('modelo'))
        equipamentoPeca = (request.form.get('equipamentoPeca'))
        equipamentoBomba = (request.form.get('equipamentoBomba'))
        entrada = (request.form.get('entrada'))
        data = (request.form.get('data'))
        observacao = (request.form.get('observacao'))

        if modelo and entrada and data or equipamentoPeca or equipamentoBomba:

            if modelo == '1':

                try:
                    bomba = TipoBomba.query.filter_by(tipo=equipamentoBomba).first()

                    total = calculaEstoqueBomba(bomba.qtEstoque, entrada)

                    estoque = EntradaEstoque(modelo=modelo, equipamento=bomba.tipo, estoqueAntigo=bomba.qtEstoque,
                                             entrada=entrada, total=total, dataEntrada=data, observacao=observacao)
                    atualizaEstoqueBomba(equipamentoBomba, total)

                    db.session.add(estoque)
                    db.session.commit()

                    flash('Inserido com sucesso!', 'info')

                except Exception as e:

                    print(e.args)

            elif modelo == '2':

                try:
                    peca = Peca.query.filter_by(descricao=equipamentoPeca).first()

                    total = calculaEstoquePeca(peca.qtEstoque, entrada)

                    estoque = EntradaEstoque(modelo=modelo, equipamento=peca.descricao, estoqueAntigo=peca.qtEstoque,
                                             entrada=entrada, total=total, dataEntrada=data, observacao=observacao)

                    atualizaEstoquePeca(equipamentoPeca, total)

                    db.session.add(estoque)
                    db.session.commit()

                    flash('Inserido com sucesso!', 'info')

                except Exception as e:

                    print(e.args)

            else:
                flash('Tipo ou modelo do equipamento não existe!', 'error')

        flash('Não foi possível inserir!', 'error')
    return redirect(url_for('entradaEstoque'))


def calculaEstoqueBomba(qtEstoque, entrada):
    total = qtEstoque + int(entrada)

    return total


def calculaEstoquePeca(qtEstoque, entrada):
    total = qtEstoque + int(entrada)

    return total


def atualizaEstoqueBomba(equipamento, total):
    bb = TipoBomba.query.filter_by(tipo=equipamento).first()
    bb.qtEstoque = total

    db.session.commit()


def atualizaEstoquePeca(equipamento, total):
    p = Peca.query.filter_by(descricao=equipamento).first()
    p.qtEstoque = total

    db.session.commit()


@app.route('/autocompleteBuscaPecas', methods=['GET'])
def autocompleteBuscaPecas():
    pecas = Peca.query.all()

    list = []
    for p in pecas:
        list.append(p.descricao)

    return Response(json.dumps(list), mimetype='application/json')
