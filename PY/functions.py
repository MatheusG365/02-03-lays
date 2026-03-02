from flask import Flask, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
import threading
import smtplib
from email.mime.text import MIMEText
import jwt, datetime
from main import app

senha_secreta = app.config['SECRET_KEY']

def gerar_token(id_usuario):
    payload = {'id_usuario': id_usuario,
            'timestamp': datetime.datetime.utcnow().isoformat()}
    token = jwt.encode(payload, senha_secreta, algorithm='HS256')

    return token

def remover_bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
        return token

def validar_senha(senha):
    maiscula = False
    minuscula = False
    caracterepcd = False
    numero = False
    quanti = False

    if len(senha) >= 8:
        quanti = True

    for c in senha:
        if c.isupper():
            maiscula = True
        if c.islower():
            minuscula = True
        if c.isdigit():
            numero = True
        if not c.isalnum():
            caracterepcd = True

    senha_v = generate_password_hash(senha).decode('utf-8')

    if maiscula and minuscula and numero and caracterepcd and quanti:
        return senha_v
    else:
        return jsonify({"error":"Senha invalida"}),400


def enviando_email(destinatario, assunto, mensagem):
    user = "matheusgdsiqui@gmail.com"
    senha = "wbmnvjnsjnppurjh"

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = user
    msg['To'] = destinatario

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, senha)
    server.send_message(msg)
    server.quit()


