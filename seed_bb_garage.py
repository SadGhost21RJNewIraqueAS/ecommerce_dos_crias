from __future__ import annotations

from sqlalchemy import delete

from database import SessionLocal
from models.carrinho import Carrinho
from models.categoria import Categoria
from models.cliente import Cliente
from models.item_carrinho import ItemCarrinho
from models.item_pedido import ItemPedido
from models.pedido import Pedido
from models.produto import Produto
from models.usuario import Usuario
from segurança import get_password_hash


CATEGORIAS = [
    (
        "Rodas",
        "Rodas esportivas e de série para diferentes modelos de veículos, com acabamento durável e visual premium.",
    ),
    (
        "Pneus",
        "Pneus para uso urbano, passeio e desempenho, com boa aderência e durabilidade em diversas condições.",
    ),
    (
        "Freios",
        "Discos, pastilhas e pinças para garantir frenagem segura e eficiente em qualquer situação.",
    ),
    (
        "Suspensão",
        "Componentes de suspensão para maior estabilidade, conforto e controle de direção do veículo.",
    ),
    (
        "Amortecedores",
        "Amortecedores de alta qualidade para melhorar o conforto e a segurança da condução.",
    ),
    (
        "Molas",
        "Molas para reposição e performance, com resistência adequada para cada tipo de uso.",
    ),
    (
        "Acessórios",
        "Acessórios automotivos para melhoria, organização e personalização do veículo.",
    ),
    (
        "Kits Automotivos",
        "Kits completos de peças para manutenção, atualização e restauração de veículos.",
    ),
]

PRODUTOS = [
    ("Roda Esportiva Volcano Aro 17", "Roda leve com acabamento em grafite para uso esportivo.", "Rodas", 1099.90, 12),
    ("Roda Esportiva KR Aro 18", "Roda premium com desenho moderno para veículos de alto desempenho.", "Rodas", 1299.90, 8),
    ("Roda Five Star Aro 15", "Roda robusta e funcional para uso urbano e passeio.", "Rodas", 899.00, 15),
    ("Roda Black Diamond Aro 16", "Roda em design agressivo para veículos com perfil esportivo.", "Rodas", 1049.00, 10),
    ("Pneu Michelin 205/55 R16", "Pneu de alto desempenho para carros de passeio com conforto e aderência.", "Pneus", 429.90, 23),
    ("Pneu Pirelli 225/45 R17", "Pneu esportivo com excelente aderência em alta velocidade.", "Pneus", 599.00, 18),
    ("Pneu Goodyear 195/65 R15", "Pneu confiável para uso diário com bom custo-benefício.", "Pneus", 319.90, 30),
    ("Pneu Continental 215/50 R17", "Pneu com tração e estabilidade para rodagem segura em diferentes condições.", "Pneus", 549.90, 20),
    ("Disco de Freio Dianteiro", "Disco de freio original para melhor frenagem e durabilidade.", "Freios", 389.00, 17),
    ("Pastilha de Freio Dianteira", "Pastilha de alta resistência para redução do desgaste de discos.", "Freios", 219.90, 25),
    ("Pastilha de Freio Traseira", "Pastilha traseira eficiente para manter equilíbrio e eficiência de frenagem.", "Freios", 209.90, 26),
    ("Pinça de Freio Esportiva", "Pinça de freio com desempenho superior e visual esportivo.", "Freios", 689.00, 9),
    ("Kit Suspensão Esportiva", "Kit completo para melhorar o controle de direção e a estabilidade.", "Suspensão", 1499.00, 7),
    ("Kit Suspensão de Rosca", "Kit de suspensão ajustável para melhor altura e comportamento do veículo.", "Suspensão", 1299.00, 8),
    ("Bucha de Bandeja", "Bucha premium para reduzir vibrações e melhorar a segurança da condução.", "Suspensão", 189.00, 33),
    ("Barra Estabilizadora", "Barra estabilizadora para maior estabilidade em curvas e frenagens.", "Suspensão", 459.90, 18),
    ("Amortecedor Dianteiro Cofap", "Amortecedor dianteiro com bom custo-benefício e alta durabilidade.", "Amortecedores", 399.00, 16),
    ("Amortecedor Traseiro Monroe", "Amortecedor traseiro para conforto e estabilidade em diversas condições.", "Amortecedores", 429.90, 14),
    ("Mola Esportiva Dianteira", "Mola dianteira com desempenho superior para veículos com uso esportivo.", "Molas", 356.00, 11),
    ("Mola Esportiva Traseira", "Mola traseira para melhor resposta e estabilidade de conjunto.", "Molas", 346.00, 12),
]

USUARIOS = [
    {"nome": "Cliente 1", "username": "cliente1", "email": "cliente1@bbgarage.com", "senha": "cliente1", "role": "cliente"},
    {"nome": "Cliente 2", "username": "cliente2", "email": "cliente2@bbgarage.com", "senha": "cliente2", "role": "cliente"},
    {"nome": "Cliente 3", "username": "cliente3", "email": "cliente3@bbgarage.com", "senha": "cliente3", "role": "cliente"},
    {"nome": "Cliente 4", "username": "cliente4", "email": "cliente4@bbgarage.com", "senha": "cliente4", "role": "cliente"},
    {"nome": "Cliente 5", "username": "cliente5", "email": "cliente5@bbgarage.com", "senha": "cliente5", "role": "cliente"},
    {"nome": "Cliente 6", "username": "cliente6", "email": "cliente6@bbgarage.com", "senha": "cliente6", "role": "cliente"},
    {"nome": "Cliente 7", "username": "cliente7", "email": "cliente7@bbgarage.com", "senha": "cliente7", "role": "cliente"},
    {"nome": "Cliente 8", "username": "cliente8", "email": "cliente8@bbgarage.com", "senha": "cliente8", "role": "cliente"},
    {"nome": "Cliente 9", "username": "cliente9", "email": "cliente9@bbgarage.com", "senha": "cliente9", "role": "cliente"},
    {"nome": "Cliente 10", "username": "cliente10", "email": "cliente10@bbgarage.com", "senha": "cliente10", "role": "cliente"},
    {"nome": "Gerente 1", "username": "gerente1", "email": "gerente1@bbgarage.com", "senha": "gerente1", "role": "gerente"},
    {"nome": "Gerente 2", "username": "gerente2", "email": "gerente2@bbgarage.com", "senha": "gerente2", "role": "gerente"},
    {"nome": "Gerente 3", "username": "gerente3", "email": "gerente3@bbgarage.com", "senha": "gerente3", "role": "gerente"},
    {"nome": "Admin 1", "username": "admin1", "email": "admin1@bbgarage.com", "senha": "admin1", "role": "admin"},
    {"nome": "Admin 2", "username": "admin2", "email": "admin2@bbgarage.com", "senha": "admin2", "role": "admin"},
]

CLIENTES = [
    {"nome": "João da Silva", "cpf": 11122233344, "email": "joao.silva@cliente.com", "tel1": 11911110001, "tel2": 11911110002},
    {"nome": "Maria Oliveira", "cpf": 22233344455, "email": "maria.oliveira@cliente.com", "tel1": 11911110003, "tel2": 11911110004},
    {"nome": "Pedro Souza", "cpf": 33344455566, "email": "pedro.souza@cliente.com", "tel1": 11911110005, "tel2": 11911110006},
    {"nome": "Ana Costa", "cpf": 44455566677, "email": "ana.costa@cliente.com", "tel1": 11911110007, "tel2": 11911110008},
    {"nome": "Lucas Pereira", "cpf": 55566677788, "email": "lucas.pereira@cliente.com", "tel1": 11911110009, "tel2": 11911110010},
    {"nome": "Fernanda Rocha", "cpf": 66677788899, "email": "fernanda.rocha@cliente.com", "tel1": 11911110011, "tel2": 11911110012},
    {"nome": "Rafael Lima", "cpf": 77788899900, "email": "rafael.lima@cliente.com", "tel1": 11911110013, "tel2": 11911110014},
    {"nome": "Beatriz Santos", "cpf": 88899900011, "email": "beatriz.santos@cliente.com", "tel1": 11911110015, "tel2": 11911110016},
    {"nome": "Gabriel Almeida", "cpf": 99900011122, "email": "gabriel.almeida@cliente.com", "tel1": 11911110017, "tel2": 11911110018},
    {"nome": "Camila Martins", "cpf": 10020030040, "email": "camila.martins@cliente.com", "tel1": 11911110019, "tel2": 11911110020},
]

CARTS = [
    {"cliente_id": 1, "valor_total": 0.0},
    {"cliente_id": 2, "valor_total": 0.0},
    {"cliente_id": 3, "valor_total": 0.0},
    {"cliente_id": 4, "valor_total": 0.0},
    {"cliente_id": 5, "valor_total": 0.0},
    {"cliente_id": 6, "valor_total": 0.0},
]

CART_ITEMS = [
    (1, 1, 2, 1099.90),
    (1, 5, 1, 429.90),
    (2, 9, 1, 389.00),
    (2, 18, 2, 429.90),
    (3, 11, 1, 209.90),
    (3, 12, 1, 689.00),
    (3, 13, 1, 1499.00),
    (4, 6, 2, 599.00),
    (4, 8, 1, 549.90),
    (5, 17, 1, 399.00),
    (5, 20, 2, 346.00),
    (6, 4, 1, 1049.00),
]

PEDIDOS = [
    {"cliente_id": 1, "status": "pendente", "forma_pagamento": "pix", "status_pagamento": "pendente", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 2, "status": "confirmado", "forma_pagamento": "cartao_credito", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 3, "status": "processando", "forma_pagamento": "cartao_debito", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 4, "status": "enviado", "forma_pagamento": "boleto", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 5, "status": "entregue", "forma_pagamento": "pix", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 6, "status": "cancelado", "forma_pagamento": "cartao_credito", "status_pagamento": "recusado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 7, "status": "pendente", "forma_pagamento": "cartao_debito", "status_pagamento": "pendente", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 8, "status": "confirmado", "forma_pagamento": "pix", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 9, "status": "processando", "forma_pagamento": "boleto", "status_pagamento": "pendente", "valor_total": 0.0, "estoque": 0},
    {"cliente_id": 10, "status": "enviado", "forma_pagamento": "pix", "status_pagamento": "aprovado", "valor_total": 0.0, "estoque": 0},
]

PEDIDO_ITENS = [
    (1, 1, 1, 1099.90),
    (1, 5, 1, 429.90),
    (2, 2, 1, 1299.90),
    (2, 12, 1, 689.00),
    (3, 9, 2, 389.00),
    (3, 10, 1, 219.90),
    (4, 6, 2, 599.00),
    (4, 13, 1, 1499.00),
    (5, 17, 1, 399.00),
    (5, 18, 1, 429.90),
    (6, 3, 1, 899.00),
    (6, 16, 1, 459.90),
    (7, 7, 2, 319.90),
    (7, 14, 1, 1299.00),
    (8, 8, 1, 549.90),
    (8, 19, 2, 356.00),
    (9, 15, 1, 189.00),
    (9, 20, 1, 346.00),
    (10, 4, 1, 1049.00),
    (10, 11, 2, 209.90),
]


def limpar_banco(session):
    session.execute(delete(ItemPedido))
    session.execute(delete(Pedido))
    session.execute(delete(ItemCarrinho))
    session.execute(delete(Carrinho))
    session.execute(delete(Cliente))
    session.execute(delete(Usuario))
    session.execute(delete(Produto))
    session.execute(delete(Categoria))
    session.commit()


def criar_usuarios(session):
    usuarios = []
    for dado in USUARIOS:
        usuarios.append(
            Usuario(
                nome=dado["nome"],
                username=dado["username"],
                email=dado["email"],
                senha_hash=get_password_hash(dado["senha"]),
                role=dado["role"],
                is_active=True,
            )
        )
    session.add_all(usuarios)
    session.flush()
    return usuarios


def criar_categorias(session):
    categorias = [Categoria(nome=nome, descricao=descricao) for nome, descricao in CATEGORIAS]
    session.add_all(categorias)
    session.flush()
    return {categoria.nome: categoria.id for categoria in categorias}


def criar_produtos(session, categoria_por_nome):
    produtos = []
    for nome, descricao, nome_categoria, valor, estoque in PRODUTOS:
        produtos.append(
            Produto(
                categoria_id=categoria_por_nome[nome_categoria],
                nome=nome,
                descricao=descricao,
                valor_produto=valor,
                estoque=estoque,
            )
        )
    session.add_all(produtos)
    session.flush()
    return produtos


def criar_clientes(session):
    clientes = [
        Cliente(
            nome=cliente["nome"],
            cpf=cliente["cpf"],
            email=cliente["email"],
            tel1=cliente["tel1"],
            tel2=cliente["tel2"],
        )
        for cliente in CLIENTES
    ]
    session.add_all(clientes)
    session.flush()
    return clientes


def criar_carrinhos(session):
    carrinhos = [
        Carrinho(cliente_id=item["cliente_id"], valor_total=item["valor_total"]) for item in CARTS
    ]
    session.add_all(carrinhos)
    session.flush()
    return carrinhos


def criar_itens_carrinho(session):
    itens = []
    for carrinho_id, produto_id, quantidade, valor_unitario in CART_ITEMS:
        itens.append(
            ItemCarrinho(
                carrinho_id=carrinho_id,
                produto_id=produto_id,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
            )
        )
    session.add_all(itens)
    session.flush()

    by_carrinho = {}
    for item in itens:
        by_carrinho.setdefault(item.carrinho_id, 0.0)
        by_carrinho[item.carrinho_id] += item.quantidade * item.valor_unitario

    for carrinho in session.query(Carrinho).all():
        if carrinho.id in by_carrinho:
            carrinho.valor_total = round(by_carrinho[carrinho.id], 2)

    session.flush()


def criar_pedidos(session):
    pedidos = [
        Pedido(
            cliente_id=item["cliente_id"],
            status=item["status"],
            forma_pagamento=item["forma_pagamento"],
            status_pagamento=item["status_pagamento"],
            valor_total=item["valor_total"],
            estoque=item["estoque"],
        )
        for item in PEDIDOS
    ]
    session.add_all(pedidos)
    session.flush()
    return pedidos


def criar_itens_pedido(session):
    itens = []
    for pedido_id, produto_id, quantidade, preco_unitario in PEDIDO_ITENS:
        itens.append(
            ItemPedido(
                pedido_id=pedido_id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
            )
        )
    session.add_all(itens)
    session.flush()

    by_pedido = {}
    for item in itens:
        by_pedido.setdefault(item.pedido_id, 0.0)
        by_pedido[item.pedido_id] += item.quantidade * item.preco_unitario

    for pedido in session.query(Pedido).all():
        if pedido.id in by_pedido:
            pedido.valor_total = round(by_pedido[pedido.id], 2)
            pedido.estoque = sum(item.quantidade for item in session.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).all())

    session.flush()


def main():
    with SessionLocal() as session:
        limpar_banco(session)
        criar_usuarios(session)
        categoria_por_nome = criar_categorias(session)
        criar_produtos(session, categoria_por_nome)
        criar_clientes(session)
        criar_carrinhos(session)
        criar_itens_carrinho(session)
        criar_pedidos(session)
        criar_itens_pedido(session)
        session.commit()

    print("SEED FINALIZADO")
    with SessionLocal() as session:
        total_usuarios = session.query(Usuario).count()
        total_clientes = session.query(Cliente).count()
        total_gerentes = session.query(Usuario).filter(Usuario.role == "gerente").count()
        total_admins = session.query(Usuario).filter(Usuario.role == "admin").count()
        total_categorias = session.query(Categoria).count()
        total_produtos = session.query(Produto).count()
        total_carrinhos = session.query(Carrinho).count()
        total_itens_carrinho = session.query(ItemCarrinho).count()
        total_pedidos = session.query(Pedido).count()
        total_itens_pedido = session.query(ItemPedido).count()

        print({
            "usuarios": total_usuarios,
            "clientes": total_clientes,
            "gerentes": total_gerentes,
            "administradores": total_admins,
            "categorias": total_categorias,
            "produtos": total_produtos,
            "carrinhos": total_carrinhos,
            "itens_carrinho": total_itens_carrinho,
            "pedidos": total_pedidos,
            "itens_pedido": total_itens_pedido,
        })


if __name__ == "__main__":
    main()
