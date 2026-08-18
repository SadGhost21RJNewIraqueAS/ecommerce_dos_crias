import os
import unittest
import uuid

from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import app
from schemas.usuario import UsuarioCreate
from segurança import create_access_token, get_password_hash, usuario_tem_permissao, verify_password


class AuthTests(unittest.TestCase):
    def test_password_hash_and_verify(self):
        senha = "minhaSenha123"
        hash_senha = get_password_hash(senha)
        self.assertNotEqual(hash_senha, senha)
        self.assertTrue(verify_password(senha, hash_senha))
        self.assertFalse(verify_password("outraSenha", hash_senha))

    def test_create_access_token(self):
        token = create_access_token({"sub": "joao@example.com", "role": "admin"})
        self.assertIsInstance(token, str)
        self.assertTrue(token)

    def test_usuario_tem_permissao(self):
        token_admin = create_access_token({"sub": "admin@example.com", "role": "admin"})
        token_gerente = create_access_token({"sub": "gerente@example.com", "role": "gerente"})
        token_cliente = create_access_token({"sub": "cliente@example.com", "role": "cliente"})

        self.assertTrue(usuario_tem_permissao(token_admin, ["admin", "gerente"]))
        self.assertTrue(usuario_tem_permissao(token_gerente, ["gerente", "admin"]))
        self.assertFalse(usuario_tem_permissao(token_cliente, ["gerente", "admin"]))

    def test_role_default_cliente(self):
        self.assertEqual("cliente", "cliente")

    def test_seed_admin_teste(self):
        original_env = os.getenv("APP_ENV")
        os.environ["APP_ENV"] = "test"
        try:
            client = TestClient(app)
            response = client.post(
                "/auth/dev/seed-admin",
                params={
                    "email": "admin_teste@teste.local",
                    "username": "admin_teste",
                    "senha": "admin123",
                },
            )
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertEqual(data["role"], "admin")
            self.assertIn("access_token", data)
        finally:
            if original_env is None:
                os.environ.pop("APP_ENV", None)
            else:
                os.environ["APP_ENV"] = original_env

    def test_login_json_usa_username_do_cadastro(self):
        client = TestClient(app)
        identificador = uuid.uuid4().hex[:8]
        username = f"maria_user_{identificador}"
        email = f"maria_user_{identificador}@example.com"

        registro = client.post(
            "/auth/registro",
            json={
                "nome": "Maria",
                "username": username,
                "email": email,
                "senha": "123456",
            },
        )
        self.assertEqual(registro.status_code, 201)

        login = client.post(
            "/auth/login",
            json={"username": username, "password": "123456"},
        )

        self.assertEqual(login.status_code, 200)
        self.assertIn("access_token", login.json())

    def test_login_form_usa_username_do_cadastro(self):
        client = TestClient(app)
        identificador = uuid.uuid4().hex[:8]
        username = f"maria_form_{identificador}"
        email = f"maria_form_{identificador}@example.com"

        registro = client.post(
            "/auth/registro",
            json={
                "nome": "Maria",
                "username": username,
                "email": email,
                "senha": "123456",
            },
        )
        self.assertEqual(registro.status_code, 201)

        login = client.post(
            "/auth/login/form",
            data={"username": username, "password": "123456"},
        )

        self.assertEqual(login.status_code, 200)
        self.assertIn("access_token", login.json())

    def test_usuario_create_nao_aceita_cpf_telefone(self):
        with self.assertRaises(ValidationError):
            UsuarioCreate.model_validate({
                "nome": "Maria",
                "username": "maria",
                "email": "maria@example.com",
                "senha": "123456",
                "cpf": "12345678901",
                "telefone": "11999999999",
            })

        usuario = UsuarioCreate.model_validate({
            "nome": "Maria",
            "username": "maria",
            "email": "maria@example.com",
            "senha": "123456",
        })
        self.assertEqual(usuario.nome, "Maria")

    def test_produto_nao_pode_ser_criado_sem_categoria_existente(self):
        client = TestClient(app)
        original_env = os.getenv("APP_ENV")
        os.environ["APP_ENV"] = "test"

        try:
            seed = client.post(
                "/auth/dev/seed-admin",
                params={
                    "email": "admin_categoria@teste.local",
                    "username": "admin_categoria",
                    "senha": "admin123",
                },
            )
            self.assertEqual(seed.status_code, 201)

            token = seed.json()["access_token"]
            response = client.post(
                "/produtos/",
                json={
                    "categoria_id": 9999,
                    "nome": "Produto teste",
                    "descricao": "Produto sem categoria válida",
                    "valor_produto": 49.9,
                    "estoque": 10,
                },
                headers={"Authorization": f"Bearer {token}"},
            )

            self.assertEqual(response.status_code, 404)
            self.assertIn("Categoria", response.json()["detail"])
        finally:
            if original_env is None:
                os.environ.pop("APP_ENV", None)
            else:
                os.environ["APP_ENV"] = original_env


if __name__ == "__main__":
    unittest.main()
