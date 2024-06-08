from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#Criação da aplicação baseada no Flask
app = Flask(__name__)
#Realiza a conexão com o banco de dados
app.config.from_pyfile('configuracao.py')
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
from rotas import *

#Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)


