from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    pais = db.Column(db.String(150))

    def __init__(self, nome, idade, pais):
        self.nome = nome
        self.idade = idade
        self.pais = pais

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    genero = db.Column(db.String(150))
    # Criando a chave estrangeira
    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'))    
    # Definindo o relacionamento
    ator = db.relationship('Ator', backref=db.backref('serie', lazy=True))

    def __init__(self, titulo, ano, genero, ator_id):
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.ator_id = ator_id
