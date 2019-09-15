from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Usuario
from werkzeug.urls import url_parse


@app.route("/index")
@login_required
def index():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #verifico se o usuario está logado ou não
        return redirect(url_for('index')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username = form.username.data).first()
        print(user.username, user.password_hash)
        if user is None or not user.check_password(form.password.data):
            print('invalido')
            flash('Usuário ou senha incorretos!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': #se tiver valor que não pertença a url principal
            next_page = url_for('index')
        return redirect(next_page) #se tiver ele direciona para onde foi solicitado
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))