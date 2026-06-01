from decimal import Decimal
from functools import wraps

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from database import db, init_db
from database.models import Imovel, Log, Usuario


app = Flask(__name__)
app.config.from_object(Config)
init_db(app)


def registrar_log(mensagem):
    """Salva eventos importantes no histórico do sistema."""
    try:
        db.session.add(Log(log=mensagem))
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()


def login_required(view):
    """Garante acesso apenas ao administrador autenticado."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            flash("Faça login para acessar a área administrativa.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def get_form_data():
    """Lê e normaliza os dados enviados pelos formulários de imóvel."""
    return {
        "tp_imovel": request.form.get("tp_imovel", "").strip(),
        "valor": Decimal(
            request.form.get("valor", "0").replace(".", "").replace(",", ".") or "0"
        ),
        "endereco": request.form.get("endereco", "").strip(),
        "cidade": request.form.get("cidade", "").strip(),
        "estado": request.form.get("estado", "").strip(),
        "quant_quartos": int(request.form.get("quant_quartos", "0") or 0),
        "vagas_garagem": int(request.form.get("vagas_garagem", "0") or 0),
        "area_m2": Decimal(request.form.get("area_m2", "0").replace(",", ".") or "0"),
        "descricao": request.form.get("descricao", "").strip(),
        "tp_transacao": request.form.get("tp_transacao", "").strip(),
        "status": request.form.get("status", "Disponivel").strip(),
    }


@app.route("/")
def home():
    termo = request.args.get("q", "").strip()
    cidade = request.args.get("cidade", "").strip()
    tp_imovel = request.args.get("tp_imovel", "").strip()
    tp_transacao = request.args.get("tp_transacao", "").strip()

    query = Imovel.query.filter(Imovel.status == "Disponivel")

    if termo:
        like_termo = f"%{termo}%"
        query = query.filter(
            (Imovel.endereco.ilike(like_termo)) | (Imovel.cidade.ilike(like_termo))
        )
    if cidade:
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))
    if tp_imovel:
        query = query.filter(Imovel.tp_imovel == tp_imovel)
    if tp_transacao:
        query = query.filter(Imovel.tp_transacao == tp_transacao)

    imoveis = query.order_by(Imovel.dt_insert.desc()).all()
    tipos = [row[0] for row in db.session.query(Imovel.tp_imovel).distinct().order_by(Imovel.tp_imovel)]

    return render_template(
        "index.html",
        imoveis=imoveis,
        termos={
            "q": termo,
            "cidade": cidade,
            "tp_imovel": tp_imovel,
            "tp_transacao": tp_transacao,
        },
        tipos=tipos,
    )


@app.route("/imovel/<int:id>")
def imovel_detalhe(id):
    imovel = Imovel.query.get_or_404(id)
    return render_template("imovel.html", imovel=imovel)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.query.filter_by(email=email, admin=True).first()
        if usuario and usuario.check_password(senha):
            session["user_id"] = usuario.codigo
            session["user_name"] = usuario.nome
            session["admin"] = True
            registrar_log(f"Login administrativo realizado por {usuario.nome} ({usuario.email}).")
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("admin"))

        registrar_log(f"Tentativa de login inválida para o email {email}.")
        flash("Credenciais inválidas.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    nome = session.get("user_name", "Administrador")
    session.clear()
    registrar_log(f"Logout administrativo realizado por {nome}.")
    flash("Sessão encerrada.", "info")
    return redirect(url_for("home"))


@app.route("/admin")
@login_required
def admin():
    total_imoveis = Imovel.query.count()
    total_usuarios = Usuario.query.count()
    total_logs = Log.query.count()
    logs = Log.query.order_by(Log.dt_insert.desc()).limit(10).all()
    imoveis = Imovel.query.order_by(Imovel.dt_insert.desc()).all()

    return render_template(
        "dashboard.html",
        total_imoveis=total_imoveis,
        total_usuarios=total_usuarios,
        total_logs=total_logs,
        logs=logs,
        imoveis=imoveis,
    )


@app.route("/admin/imovel/novo", methods=["GET", "POST"])
@login_required
def novo_imovel():
    if request.method == "POST":
        dados = get_form_data()
        if not all([dados["tp_imovel"], dados["endereco"], dados["cidade"], dados["estado"], dados["descricao"], dados["tp_transacao"]]):
            flash("Preencha todos os campos obrigatórios.", "warning")
            return render_template("imovel_form.html", imovel=None, acao="novo")

        try:
            imovel = Imovel(**dados)
            db.session.add(imovel)
            db.session.commit()
            registrar_log(f"Imóvel cadastrado: {imovel.tp_imovel} em {imovel.endereco}.")
            flash("Imóvel cadastrado com sucesso.", "success")
            return redirect(url_for("admin"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Não foi possível cadastrar o imóvel.", "danger")

    return render_template("imovel_form.html", imovel=None, acao="novo")


@app.route("/admin/imovel/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_imovel(id):
    imovel = Imovel.query.get_or_404(id)

    if request.method == "POST":
        dados = get_form_data()
        if not all([dados["tp_imovel"], dados["endereco"], dados["cidade"], dados["estado"], dados["descricao"], dados["tp_transacao"]]):
            flash("Preencha todos os campos obrigatórios.", "warning")
            return render_template("imovel_form.html", imovel=imovel, acao="editar")

        try:
            for campo, valor in dados.items():
                setattr(imovel, campo, valor)
            db.session.commit()
            registrar_log(f"Imóvel atualizado: #{imovel.codigo} - {imovel.tp_imovel}.")
            flash("Imóvel atualizado com sucesso.", "success")
            return redirect(url_for("admin"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Não foi possível atualizar o imóvel.", "danger")

    return render_template("imovel_form.html", imovel=imovel, acao="editar")


@app.route("/admin/imovel/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_imovel(id):
    imovel = Imovel.query.get_or_404(id)

    try:
        db.session.delete(imovel)
        db.session.commit()
        registrar_log(f"Imóvel excluído: #{imovel.codigo} - {imovel.tp_imovel}.")
        flash("Imóvel excluído com sucesso.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Não foi possível excluir o imóvel.", "danger")

    return redirect(url_for("admin"))


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(_error):
    return render_template(
        "index.html",
        imoveis=[],
        termos={"q": "", "cidade": "", "tp_imovel": "", "tp_transacao": ""},
        tipos=[],
        erro="O recurso solicitado não foi encontrado.",
    ), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template(
        "index.html",
        imoveis=[],
        termos={"q": "", "cidade": "", "tp_imovel": "", "tp_transacao": ""},
        tipos=[],
        erro="Encontramos um erro inesperado. Tente novamente em instantes.",
    ), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )