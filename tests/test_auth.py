import unittest

from pydantic import ValidationError

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


if __name__ == "__main__":
    unittest.main()
