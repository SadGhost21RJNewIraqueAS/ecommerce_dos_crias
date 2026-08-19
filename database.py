from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

URL_BANCO = "sqlite:///bb_garage.db"
engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def ensure_usuario_columns(engine):
    with engine.begin() as conn:
        insp = inspect(conn)
        if "usuario" not in insp.get_table_names():
            return

        colunas = {coluna["name"]: coluna for coluna in insp.get_columns("usuario")}
        campos_necessarios = {"username", "email", "senha_hash", "role", "is_active"}
        campos_removidos = {"cpf", "telefone"}
        precisa_rebuild = any(campo not in colunas for campo in campos_necessarios) or any(
            campo in colunas for campo in campos_removidos
        )

        if not precisa_rebuild:
            return

        conn.execute(text('ALTER TABLE usuario RENAME TO usuario_antigo'))
        conn.execute(
            text(
                """
                CREATE TABLE usuario (
                    id INTEGER NOT NULL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    senha_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'cliente',
                    is_active BOOLEAN NOT NULL DEFAULT 1
                )
                """
            )
        )

        campos_insert = [
            "id",
            "nome",
            "username",
            "email",
            "senha_hash",
            "role",
            "is_active",
        ]

        valores = []
        for campo in campos_insert:
            if campo == "id":
                valores.append("id")
            elif campo == "nome":
                valores.append("nome")
            elif campo == "username":
                valores.append("COALESCE(username, 'user_' || CAST(id AS VARCHAR))")
            elif campo == "email":
                valores.append("email")
            elif campo == "senha_hash":
                valores.append("senha_hash")
            elif campo == "role":
                valores.append("COALESCE(role, 'cliente')")
            elif campo == "is_active":
                valores.append("COALESCE(is_active, 1)")

        sql = (
            "INSERT INTO usuario (" + ", ".join(campos_insert) + ") "
            "SELECT " + ", ".join(valores) + " FROM usuario_antigo"
        )
        conn.execute(text(sql))
        conn.execute(text('DROP TABLE usuario_antigo'))


def ensure_cliente_columns(engine):
    with engine.begin() as conn:
        insp = inspect(conn)
        if "cliente" not in insp.get_table_names():
            return

        colunas = {coluna["name"] for coluna in insp.get_columns("cliente")}
        if "foto" not in colunas:
            conn.execute(text("ALTER TABLE cliente ADD COLUMN foto VARCHAR"))


class Base(DeclarativeBase):
    pass
