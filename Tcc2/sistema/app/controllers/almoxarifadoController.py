from flask import render_template, url_for, redirect, request, flash, jsonify, Response
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca, EntradaEstoque
from sqlalchemy import update
import json
@app.route('/entradaEstoque', methods=['GET', 'POST'])
def entradaEstoque():

        pecas = Peca.query.all()
        bombas = TipoBomba.query.all()

        return render_template('almoxarifado/entradaProduto.html', icone="fas fa-warehouse", pecas=pecas, bombas=bombas, bloco1='Almoxarifado', bloco2="Entrada")

@app.route('/entradaProduto', methods=['GET','POST'])
def entradaProduto():

        if request.method == 'POST':

                modelo = (request.form.get('modelo'))
                equipamentoPeca = (request.form.get('equipamentoPeca'))
                equipamentoBomba = (request.form.get('equipamentoBomba'))
                estoque = (request.form.get('estoque'))
                entrada = (request.form.get('entrada'))
                total = (request.form.get('total'))
                data = (request.form.get('data'))
                observacao = (request.form.get('observacao'))

                if modelo and entrada and estoque and total and data or equipamentoPeca or equipamentoBomba:

                        if modelo == '1':

                                bomba = TipoBomba.query.filter_by(id=equipamentoBomba).first()

                                estoque = EntradaEstoque(modelo=modelo, equipamento=bomba.tipo, estoqueAntigo=estoque,
                                                         entrada=entrada, total=total, dataEntrada=data, observacao=observacao)
                                atualizaEstoqueBomba(equipamentoBomba, total)

                                db.session.add(estoque)
                                db.session.commit()

                                flash('Inserido com sucesso!', 'info')
                                return redirect(url_for('entradaEstoque'))

                        elif modelo == '2':

                                peca = Peca.query.filter_by(id=equipamentoPeca).first()

                                print('selct;', peca)
                                estoque = EntradaEstoque(modelo=modelo, equipamento=peca.descricao, estoqueAntigo=estoque,
                                                         entrada=entrada, total=total, dataEntrada=data, observacao=observacao)

                                atualizaEstoquePeca(equipamentoPeca, total)

                                db.session.add(estoque)
                                db.session.commit()

                                flash('Inserido com sucesso!', 'info')
                                return redirect(url_for('entradaEstoque'))

                        else:
                                flash('Tipo ou modelo do equipamento não existe!', 'error')
                                return redirect(url_for('entradaEstoque'))

                flash('Não foi possível realizar a operação', 'error')

        return redirect(url_for('entradaEstoque'))

def atualizaEstoqueBomba(equipamento, total):

        bb = TipoBomba.query.filter_by(id=equipamento).first()
        bb.qtEstoque = total

        db.session.commit()

def atualizaEstoquePeca(equipamento, total):

        p = Peca.query.filter_by(id=equipamento).first()
        p.qtEstoque = total

        db.session.commit()


@app.route('/autocompleteBombas', methods=['GET'])
def autocompleteBombas():

        bombas = TipoBomba.query.all()

        lista = []
        for b in bombas:
                lista.append({'id': b.id, 'qtEstoque': b.qtEstoque, 'tipo': b.tipo})


        return Response(json.dumps(lista), mimetype='application/json')

@app.route('/autocompletePecas', methods=['GET'])
def autocompletePecas():

        pecas = Peca.query.all()

        listapecas = []
        for p in pecas:
                nome = p.nome
                tipoDescricao = p.descricao
                descricao = nome + " - " + tipoDescricao
                listapecas.append({'id': p.id, 'qtEstoque': p.qtEstoque, 'tipo': descricao})

        lines = sorted(listapecas, key=lambda k: k['tipo'], reverse=False)

        return Response(json.dumps(lines), mimetype='application/json')
