use imobiliaria_marketplace;

CREATE TABLE
    usuario (
        codigo INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        telefone VARCHAR(30),
        senha VARCHAR(255) NOT NULL,
        admin BOOLEAN DEFAULT FALSE,
        dt_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        dt_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

CREATE TABLE
    log (
        codigo INT AUTO_INCREMENT PRIMARY KEY,
        log TEXT NOT NULL,
        dt_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    imoveis (
        codigo INT AUTO_INCREMENT PRIMARY KEY,
        tp_imovel VARCHAR(50) NOT NULL,
        valor DECIMAL(12, 2) NOT NULL,
        endereco VARCHAR(255) NOT NULL,
        cidade VARCHAR(100),
        estado VARCHAR(100),
        quant_quartos INT DEFAULT 0,
        vagas_garagem INT DEFAULT 0,
        area_m2 DECIMAL(10, 2),
        descricao TEXT,
        tp_transacao ENUM ('Venda', 'Aluguel') NOT NULL,
        status ENUM ('Disponivel', 'Vendido', 'Alugado', 'Inativo') DEFAULT 'Disponivel',
        dt_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        dt_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

INSERT INTO
    usuario (nome, email, telefone, senha, admin)
VALUES
    (
        'Administrador',
        'admin@imobiliaria.com',
        '(11)99999-9999',
        'admin123',
        TRUE
    );

INSERT INTO
    imoveis (
        tp_imovel,
        valor,
        endereco,
        cidade,
        estado,
        quant_quartos,
        vagas_garagem,
        area_m2,
        descricao,
        tp_transacao,
        status
    )
VALUES
    (
        'Casa',
        450000.00,
        'Rua das Palmeiras, 120',
        'São Paulo',
        'SP',
        3,
        2,
        150.00,
        'Casa ampla com quintal e churrasqueira.',
        'Venda',
        'Disponivel'
    ),
    (
        'Apartamento',
        2800.00,
        'Av. Paulista, 1000',
        'São Paulo',
        'SP',
        2,
        1,
        75.00,
        'Apartamento mobiliado próximo ao metrô.',
        'Aluguel',
        'Disponivel'
    ),
    (
        'Sobrado',
        650000.00,
        'Rua dos Ipês, 45',
        'Campinas',
        'SP',
        4,
        3,
        220.00,
        'Sobrado com piscina e área gourmet.',
        'Venda',
        'Disponivel'
    ),
    (
        'Apartamento',
        520000.00,
        'Rua XV de Novembro, 210',
        'Curitiba',
        'PR',
        3,
        2,
        110.00,
        'Apartamento em região central.',
        'Venda',
        'Disponivel'
    ),
    (
        'Casa',
        1800.00,
        'Rua das Flores, 89',
        'Londrina',
        'PR',
        2,
        1,
        90.00,
        'Casa para locação em bairro residencial.',
        'Aluguel',
        'Disponivel'
    );