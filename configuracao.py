import os

SECRET_KEY = 'teste123'
#Configuração da conexão com o banco de dados
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'bruno',
        senha = '1234',
        servidor = 'localhost',
        database = 'votacao'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

