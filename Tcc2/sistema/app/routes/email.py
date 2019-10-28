from flask_mail import Message
from app import mail, app
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.models import Usuario
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Foi enviado uma nova senha para o seu e-mail!', 'info')
        return redirect(url_for('login'))
    return render_template('novaSenha.html',
                           title='Reset Password', form=form)


def send_email(subject, sender, recipients, html_body):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    senha = '1234'
    send_email('Nova senha',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               html_body=render_template('email/alteraSenha.html',
                                         user=user, senha=senha))
