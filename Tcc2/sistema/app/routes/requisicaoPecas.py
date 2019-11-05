from flask import render_template, url_for, redirect, request, flash
from app import app, db
from app.models import Peca, TipoBomba, Requisicao
from app.forms import RequisicaoForm
from flask_login import login_required, current_user

@app.route('/requisicao/novo', methods=['GET', 'POST'])
@login_required
def requisicao():
    form = RequisicaoForm()

    if request.method == "POST":

        try:
            if form.tipoEquipamento.data == 1:
                requisicao = Requisicao(requisitante=current_user.id, tipoEquipamento=True, equipamento=form.bomba.data,
                                        quantidade=form.quantidade.data, observacao=form.observacao.data)

                db.session.add(requisicao)
                db.session.commit()
                flash('Envida com sucesso!', 'info')
                return redirect(url_for('requisicao'))

            if form.tipoEquipamento.data == 2:

                requisicao = Requisicao(requisitante=current_user.id, tipoEquipamento=False, equipamento=form.peca.data,
                                        quantidade=form.quantidade.data, observacao=form.observacao.data)

                db.session.add(requisicao)
                db.session.commit()
                flash('Envida com sucesso!', 'info')
                return redirect(url_for('requisicao'))

            else:
                flash('Tipo equipamento inválido!', 'error')
                return redirect(url_for('requisicao'))

        except Exception as e:
            flash('Um erro aconteceu. Tente novamente!', 'error')

    return render_template('requisicao/novo.html', title='Requisição', form=form)
