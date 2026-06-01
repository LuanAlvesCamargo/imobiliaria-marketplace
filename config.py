import os
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(path=".env"):
        if not os.path.exists(path):
            return False

        with open(path, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue

                chave, valor = linha.split("=", 1)
                chave = chave.strip()
                valor = valor.strip().strip("'").strip('"')
                os.environ.setdefault(chave, valor)

        return True


load_dotenv()


class Config:
    """Configurações centrais do aplicativo."""

    SECRET_KEY = os.getenv("SECRET_KEY", "imobiliaria-marketplace-chave-secreta")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "imobiliaria_marketplace")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }
