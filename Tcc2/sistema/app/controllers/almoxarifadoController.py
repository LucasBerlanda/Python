from flask import render_template, url_for, redirect, request, flash, json, jsonify
from app import app, db
from app.models import Peca, TipoBomba, Bomba_peca, Peca
from app.forms import BuscaBombasIntercambiaveis_byTipo
from flask_login import login_required

@app.route('/entradaEstoque', methods=['GET', 'POST'])
def entradaEstoque():

        return render_template('almoxarifado/entradaProduto.html')