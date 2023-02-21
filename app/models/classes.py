from app import db

class participantes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(12), unique=True, nullable=False)
    nascimento = db.Column(db.Integer, unique=True, nullable=False)
    genero = db.Column(db.String(30), unique=True, nullable=False)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Participante %r>' % self.usuario


class organizadores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    cnpj = db.Column(db.String(12), unique=True, nullable=False)
    ramo = db.Column(db.String(30), unique=True, nullable=False)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Organizador %r>' % self.usuario


class eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(120), unique=True, nullable=False)
    data = db.Column(db.Integer, unique=True, nullable=False)
    local = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.String(120), unique=True, nullable=False)
    ingressos = db.Column(db.Integer, unique=True, nullable=False)
    preco = db.Column(db.Integer, unique=True, nullable=False)
    organizador = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Evento %r>' % self.titulo
