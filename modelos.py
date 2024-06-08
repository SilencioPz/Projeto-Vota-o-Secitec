from escola import db

# Definição dos modelos
class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    votos_rel = db.relationship('Voto', backref='candidato', lazy=True)  # Renomeado para 'votos_rel'

    def __repr__(self):
        return '<Candidato %r>' % self.nome

class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    candidato_rel = db.relationship('Candidato', backref=db.backref('votos', lazy=True))  # Renomeado para 'candidato_rel'

    def __repr__(self):
        return '<Voto %r>' % self.id
