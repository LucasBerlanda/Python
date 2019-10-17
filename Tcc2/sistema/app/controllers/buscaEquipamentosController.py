from flask import render_template, Response, request
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca
from app.forms import BuscaBombasIntercambiaveis_byTipo
import json


@app.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
    
    form = BuscaBombasIntercambiaveis_byTipo()
    
    if form.validate_on_submit():
        #pega a bomba que foi filtrada
        bomba = TipoBomba.query.filter_by(tipo=form.buscaEquipamentos.data).first()

        if bomba: 
            pecasBombaSelecionada = db.session.query(Peca).join(Peca.bomba_peca).filter(Bomba_peca.tipoBomba_id==bomba.id)        
           
            if pecasBombaSelecionada:
                # filtro as peças que preciso dessa bomba para verificar as compativeis
                byRolamento = bombasByRolamento(pecasBombaSelecionada)
                byEixo = bombasByEixo(pecasBombaSelecionada)
                byBucha = bombasByBucha(pecasBombaSelecionada)
            
                tipoBombasCompativeis = getBombasCompativeis(byRolamento, byBucha, byEixo, bomba.id)
                
                return render_template('busca/equipamentos.html', form=form, pecas=pecasBombaSelecionada, tipoBombasCompativeis=tipoBombasCompativeis)

    return render_template('busca/equipamentos.html', form=form, icone="fas fa-search", bloco1='Busca de Bombas', bloco2='Peças Intercambiáveis')

def bombasByRolamento(pecas):
    # Busca id da peça com nome Rolamento na lista de peças da bomba filtrada
    for peca in pecas:
        if peca.nome == 'Rolamento':
            rolamento = peca.id
    
    bombasPossuiesseRolamento = db.session.query(TipoBomba).join(TipoBomba.bomba_peca).filter(Bomba_peca.peca_id == rolamento)
    
    if bombasPossuiesseRolamento:
        return bombasPossuiesseRolamento
    
    return ''
    
def bombasByEixo(pecas):
    # Busca id da peça com nome Eixo na lista de peças da bomba filtrada
    for peca in pecas:
        if peca.nome == 'Eixo':
            eixo = peca.id
            
    bombasPossuiesseEixo = db.session.query(TipoBomba).join(TipoBomba.bomba_peca).filter(Bomba_peca.peca_id==eixo)
    
    if bombasPossuiesseEixo:
        return bombasPossuiesseEixo
    
    return ''

def bombasByBucha(pecas):
    # Busca id da peça com nome bucha na lista de peças da bomba filtrada
    for peca in pecas:
        if peca.nome == 'Bucha':
            bucha = peca.id
    
    bombasPossuiessaBucha = db.session.query(TipoBomba).join(TipoBomba.bomba_peca).filter(Bomba_peca.peca_id==bucha)
    
    if bombasPossuiessaBucha:
        return bombasPossuiessaBucha
    
    return ''

def getBombasCompativeis(bombasRolamento, bombasEixo, bombasBucha, idBombaFiltrada):
    # É recebido 3 listas de com id das bombas que possui rolamento, eixo e bucha iguais da bomba filtrada
    
    #Percorido as listas verificando se algum id da bomba é igual para as 3 listas
    # se for alguma igual nas 3 listas é por que é compatível com a bba filtrada
    idBombasCompativeis = []
    
    for br in bombasRolamento:
        idbomasRolamento = br.id
        for Be in bombasEixo:
            if Be.id == idbomasRolamento:
                idbombasEixo = idbomasRolamento
                for bb in bombasBucha:
                    if bb.id == idbombasEixo:
                        idBombasCompativeis.append(idbombasEixo)
    
    # Pega as bombas que compativeis referente a lista de id de bombas filtrados acima 
    bombasCompativeis = []                   
    for idBbs in idBombasCompativeis:
        if idBbs != idBombaFiltrada:
            bombasCompativeis.append(TipoBomba.query.filter_by(id=idBbs).first())
    
    if bombasCompativeis:
        return bombasCompativeis
    
    return ''

@app.route('/autocompleteBuscaBombas', methods=['GET'])
def autocompleteBuscaBombas():

    bomba = TipoBomba.query.all()

    list = []
    for b in bomba:
        list.append(b.tipo)

    return Response(json.dumps(list), mimetype='application/json')
