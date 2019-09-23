from flask import render_template, url_for, redirect, request, flash, json, jsonify
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca, EntradaEstoque
from sqlalchemy import update

@app.route('/entradaEstoque', methods=['GET', 'POST'])
def entradaEstoque():

        pecas = Peca.query.all()
        bombas = TipoBomba.query.all()

        return render_template('almoxarifado/entradaProduto.html', pecas = pecas, bombas = bombas)

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
                print("modelo", modelo)
                print(equipamento)
                print(estoque)
                print(entrada)
                print(total)
                print(data)
                print(observacao)


                if modelo == '1':
                        print('primeiro if')
                        bomba = TipoBomba.query.filter_by(id = equipamento).first()
                        print("bomba", bomba.tipo)

                        estoque = EntradaEstoque(modelo=modelo, equipamento=bomba.tipo, estoqueAntigo=estoque,
                                                 entrada=entrada, total=total, dataEntrada=data, observacao=observacao)

                        atualizaEstoqueBomba(equipamento, total)

                        db.session.add(estoque)
                        db.session.commit()

                elif modelo == '2':
                        print('segundo if')
                        peca = Peca.query.filter_by(id=equipamento).first()
                        print("peca", peca.tipo)

                        estoque = EntradaEstoque(modelo=modelo, equipamento=bomba.tipo, estoqueAntigo=estoque,
                                                 entrada=entrada, total=total, dataEntrada=data, observacao=observacao)

                        atualizaEstoquePeca(equipamento, total)

                        db.session.add(estoque)
                        db.session.commit()

                else:
                        print('terceiro if')

                        flash('Tipo ou modelo do equipamento não existe!', 'error')
                        return redirect(url_for('entradaEstoque'))

                flash('Inserido com sucesso!', 'info')
                return redirect(url_for('entradaEstoque'))


def atualizaEstoqueBomba(equipamento, total):

        bb = TipoBomba.query.filter_by(id=equipamento).first()

        bb.qtEstoque = total

        db.session.commit()


def atualizaEstoquePeca(equipamento, total):

        p = update(Peca).where(Peca.id == equipamento).values(qtEstoque=total)

        db.session.commit()
