import os
from escola import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired

class FormularioCandidato(FlaskForm):
    nome = StringField('Nome do Candidato:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    descricao = StringField('Descrição do Candidato:', [validators.DataRequired(), validators.Length(min=1, max=120)])
    imagem = FileField('Imagem do Candidato:', validators=[FileAllowed(['png'], 'Images only!')])
    salvar = SubmitField('Cadastrar')

class FormularioVoto(FlaskForm):
    candidato_id = StringField('ID do Candidato:', [validators.DataRequired()])
    votar = SubmitField('Votar')

def recuperaImagem(id):
    for nomeArquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nomeArquivo:
            return nomeArquivo
    return 'padrao.png'

def deletaArquivo(id):
    arquivo = recuperaImagem(id)
    if arquivo != 'padrao.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))