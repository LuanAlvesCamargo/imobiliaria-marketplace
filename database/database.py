from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError


db = SQLAlchemy()


def init_db(app):
    """Inicializa a conexão com o banco e garante dados mínimos locais."""
    db.init_app(app)

    with app.app_context():
        try:
            from .models import Imovel, Usuario
            from werkzeug.security import generate_password_hash

            db.create_all()
        except OperationalError as error:
            raise RuntimeError(
                "Não foi possível conectar ao MariaDB. Verifique se o serviço está ativo "
                "e se DB_HOST, DB_NAME, DB_USER e DB_PASSWORD estão corretos."
            ) from error

        if not Usuario.query.filter_by(email="admin@imobiliaria.com").first():
            admin = Usuario(
                nome="Administrador",
                email="admin@imobiliaria.com",
                telefone="(11) 99999-9999",
                admin=True,
            )
            admin.senha = generate_password_hash("admin123")
            db.session.add(admin)
        else:
            admin = Usuario.query.filter_by(email="admin@imobiliaria.com").first()
            if admin and not admin.has_hashed_password():
                admin.senha = generate_password_hash(admin.senha or "admin123")

        if not Imovel.query.first():
            exemplos = [
                Imovel(
                    tp_imovel="Apartamento",
                    valor=850000,
                    endereco="Av. Paulista, 1000",
                    cidade="São Paulo",
                    estado="SP",
                    quant_quartos=3,
                    vagas_garagem=2,
                    area_m2=118,
                    descricao="Apartamento elegante em localização premium, com varanda gourmet.",
                    tp_transacao="Venda",
                    status="Disponivel",
                ),
                Imovel(
                    tp_imovel="Casa",
                    valor=4200,
                    endereco="Rua das Acácias, 245",
                    cidade="Campinas",
                    estado="SP",
                    quant_quartos=4,
                    vagas_garagem=3,
                    area_m2=240,
                    descricao="Casa ampla para aluguel, ideal para famílias que valorizam conforto.",
                    tp_transacao="Aluguel",
                    status="Disponivel",
                ),
                Imovel(
                    tp_imovel="Cobertura",
                    valor=1650000,
                    endereco="Rua Bahia, 87",
                    cidade="Curitiba",
                    estado="PR",
                    quant_quartos=4,
                    vagas_garagem=3,
                    area_m2=280,
                    descricao="Cobertura com área gourmet, vista panorâmica e acabamentos sofisticados.",
                    tp_transacao="Venda",
                    status="Disponivel",
                ),
            ]
            db.session.add_all(exemplos)

        db.session.commit()
