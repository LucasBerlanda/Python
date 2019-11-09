from flask import render_template, url_for, redirect, request, flash
from app import app, db
from app.models import Peca, TipoBomba, Requisicao, Usuario
from app.forms import RequisicaoForm
from flask_login import login_required, current_user
import datetime

@app.route('/requisicao/novo', methods=['GET', 'POST'])
@login_required
def requisicao():
    form = RequisicaoForm()

    if request.method == "POST":

        try:
            if form.tipoEquipamento.data == 1:
                requisicao = Requisicao(requisitante=current_user.id, tipoEquipamento=True, equipamento=form.bomba.data,
                                        quantidade=form.quantidade.data, observacao=form.observacao.data, dataHoraCriacao=datetime.datetime.now())

                db.session.add(requisicao)
                db.session.commit()
                flash('Envida com sucesso!', 'info')
                return redirect(url_for('requisicao'))

            if form.tipoEquipamento.data == 2:

                requisicao = Requisicao(requisitante=current_user.id, tipoEquipamento=False, equipamento=form.peca.data,
                                        quantidade=form.quantidade.data, observacao=form.observacao.data, dataHoraCriacao=datetime.datetime.now())

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


@app.route('/requisicoes/abertas', methods=['GET', 'POST'])
@login_required
def requisicoesAbertas():

    users = Usuario.query.all()
    page = request.args.get('page', 1, type=int)
    requisicoes = Requisicao.query.filter_by(pendente=True).order_by(Requisicao.dataHoraCriacao).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('requisicoesAbertas', page=requisicoes.next_num) \
        if requisicoes.has_next else None
    prev_url = url_for('requisicoesAbertas', page=requisicoes.prev_num) \
        if requisicoes.has_prev else None

    return render_template("requisicao/abertas.html", lista=requisicoes.items, next_url=next_url, prev_url=prev_url,
                           title='Requisições abertas', users=users)


@app.route("/baixarEstoque/<int:id>", methods=['GET', 'POST'])
@login_required
def baixarEstoque(id):
    requisicao = Requisicao.query.filter_by(id=id).first()

    if requisicao and requisicao.pendente is True:

        tipoequipamento = requisicao.tipoEquipamento
        equipamento = requisicao.equipamento
        quantidade = requisicao.quantidade

        if tipoequipamento == 1:
            try:
                # metodo que verifica e atualiza o estoque se possível
                atBomba = atualizaEstoqueBomba(equipamento, quantidade)

                if atBomba is True:
                    requisicao.pendente=False
                    db.session.commit()

                    flash('Dado baixa com sucesso!', 'info')
                    return redirect(url_for("requisicoesAbertas"))

            except Exception as e:
                print(e)
                flash('Não foi possível efetuar a baixa!', 'error')

        if tipoequipamento == 0:

            try:

                # metodo que verifica e atualiza o estoque se possível
                atPeca = atualizaEstoquePeca(equipamento, quantidade)

                if atPeca is True:

                    requisicao.pendente=False
                    db.session.commit()

                    flash('Dado baixa com sucesso!', 'info')
                    return redirect(url_for("requisicoesAbertas"))

            except Exception as e:
                print(e)
                flash('Não foi possível efetuar a baixa!', 'error')

    return redirect(url_for("requisicoesAbertas"))


@app.route("/excluirRequisicao/<int:id>", methods=['GET', 'POST'])
@login_required
def excluirRequisicao(id):

    requisicao = Requisicao.query.filter_by(id=id).first()

    if requisicao:

        db.session.delete(requisicao)
        db.session.commit()
        flash("Requisição removida com sucesso!", 'info')
        return redirect(url_for("requisicoesAbertas"))

    flash("Não é possível remove-la!", 'error')
    return redirect(url_for('listaPecas'))


# metodo atualiza estoque bomba
def atualizaEstoqueBomba(equipamento, quantidade):

    b = TipoBomba.query.filter_by(tipo=equipamento).first()

    qtEstoque = b.qtEstoque

    if quantidade <= qtEstoque:

        try:
            b.qtEstoque = qtEstoque - quantidade
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            flash('Ocorreu um problema!', 'error')
            return False
    else:
        flash('Quantidade em estoque insuficiente!', 'error')
        return False

# metodo atualiza estoque peca
def atualizaEstoquePeca(equipamento, quantidade):

    p = Peca.query.filter_by(descricao=equipamento).first()
    qtEstoque = p.qtEstoque

    if quantidade <= qtEstoque:

        try:
            p.qtEstoque = qtEstoque - quantidade
            db.session.commit()
            return True

        except Exception as e:

            print(e)
            flash('Ocorreu um problema!', 'error')
            return False
    else:
        flash('Quantidade em estoque insuficiente!', 'error')
        return False


@app.route('/requisicoes/baixadas', methods=['GET', 'POST'])
@login_required
def requisicoesBaixadas():

    users = Usuario.query.all()
    page = request.args.get('page', 1, type=int)
    requisicoes = Requisicao.query.filter_by(pendente=False).order_by(Requisicao.dataHoraCriacao).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('requisicoesBaixadas', page=requisicoes.next_num) \
        if requisicoes.has_next else None
    prev_url = url_for('requisicoeBaixadas', page=requisicoes.prev_num) \
        if requisicoes.has_prev else None

    return render_template("requisicao/baixadas.html", lista=requisicoes.items, next_url=next_url, prev_url=prev_url,
                           title='Requisições baixadas', users=users)


@app.route('/requisicoes/todas', methods=['GET', 'POST'])
@login_required
def requisicoesTodas():

    users = Usuario.query.all()
    page = request.args.get('page', 1, type=int)
    requisicoes = Requisicao.query.order_by(Requisicao.dataHoraCriacao).paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('requisicoesTodas', page=requisicoes.next_num) \
        if requisicoes.has_next else None
    prev_url = url_for('requisicoesTodas', page=requisicoes.prev_num) \
        if requisicoes.has_prev else None

    return render_template("requisicao/Todas.html", lista=requisicoes.items, next_url=next_url, prev_url=prev_url,
                           title='Todas as requisições', users=users)