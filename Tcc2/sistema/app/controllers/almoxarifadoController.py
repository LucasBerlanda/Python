from flask import render_template, url_for, redirect, request, flash, json, jsonify
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca, EntradaEstoque
from sqlalchemy import update

@app.route('/entradaEstoque', methods=['GET', 'POST'])
def entradaEstoque():

        pecas = Peca.query.all()
        bombas = TipoBomba.query.all()

        return render_template('almoxarifado/entradaProduto.html', icone="fas fa-warehouse", pecas=pecas, bombas=bombas, bloco1='Almoxarifado', bloco2="Entrada")

@app.route('/entradaProduto', methods=['GET','POST'])
def entradaProduto():

        if request.method == 'POST':
                modelo = (request.form.get('modelo'))
                equipamento = (request.form.get('equipamento'))
                estoque = (request.form.get('estoque'))
                entrada = (request.form.get('entrada'))
                total = (request.form.get('total'))
                data = (request.form.get('data'))
                observacao = (request.form.get('observacao'))

                if modelo == '1':

                        bomba = TipoBomba.query.filter_by(id=equipamento).first()

                        estoque = EntradaEstoque(modelo=modelo, equipamento=bomba.tipo, estoqueAntigo=estoque,
                                                 entrada=entrada, total=total, dataEntrada=data, observacao=observacao)
                        atualizaEstoqueBomba(equipamento, total)

                        db.session.add(estoque)
                        db.session.commit()

                        flash('Inserido com sucesso!', 'info')

                elif modelo == '2':

                        peca = Peca.query.filter_by(id=equipamento).first()

                        estoque = EntradaEstoque(modelo=modelo, equipamento=peca.descricao, estoqueAntigo=estoque,
                                                 entrada=entrada, total=total, dataEntrada=data, observacao=observacao)

                        atualizaEstoquePeca(equipamento, total)

                        db.session.add(estoque)
                        db.session.commit()

                        flash('Inserido com sucesso!', 'info')

                else:
                        flash('Tipo ou modelo do equipamento não existe!', 'error')
                        return redirect(url_for('entradaEstoque'))


                return redirect(url_for('entradaEstoque'))


def atualizaEstoqueBomba(equipamento, total):

        bb = TipoBomba.query.filter_by(id=equipamento).first()

        bb.qtEstoque = total

        db.session.commit()


def atualizaEstoquePeca(equipamento, total):

        p = Peca.query.filter_by(id=equipamento).first()

        p.qtEstoque = total

        db.session.commit()
