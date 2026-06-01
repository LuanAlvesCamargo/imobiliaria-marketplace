# Imobiliária Marketplace

Sistema web completo para venda e aluguel de imóveis, desenvolvido com Flask, SQLAlchemy, MariaDB, Bootstrap 5, HTML, CSS e JavaScript.

## Execução local

1. Crie o banco `imobiliaria_marketplace` no MariaDB.
2. Copie `.env.example` para `.env` e ajuste as credenciais do MariaDB.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python app.py
```

## Login administrativo padrão

- E-mail: `admin@imobiliaria.com`
- Senha: `admin123`

## Estrutura principal

- `app.py` — rotas e regras de negócio
- `config.py` — configuração do projeto
- `database/` — conexão com o banco e modelos
- `templates/` — páginas Jinja2
- `static/` — CSS, JavaScript e imagens
