from werkzeug.security import check_password_hash, generate_password_hash

from .database import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    telefone = db.Column(db.String(30))
    senha = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    dt_insert = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    dt_update = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        if not self.senha:
            return False
        if self.senha.startswith(("pbkdf2:", "scrypt:", "argon2:")):
            return check_password_hash(self.senha, password)
        return self.senha == password

    def has_hashed_password(self):
        return bool(self.senha) and self.senha.startswith(("pbkdf2:", "scrypt:", "argon2:"))


class Log(db.Model):
    __tablename__ = "log"

    codigo = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.Text, nullable=False)
    dt_insert = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )


class Imovel(db.Model):
    __tablename__ = "imoveis"

    codigo = db.Column(db.Integer, primary_key=True)
    tp_imovel = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Numeric(12, 2), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    quant_quartos = db.Column(db.Integer, default=0, nullable=False)
    vagas_garagem = db.Column(db.Integer, default=0, nullable=False)
    area_m2 = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tp_transacao = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Disponivel", nullable=False)
    dt_insert = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    dt_update = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def valor_formatado(self):
        return f"R$ {float(self.valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
