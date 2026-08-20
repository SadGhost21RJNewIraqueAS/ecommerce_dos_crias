import os
import logging
from dotenv import load_dotenv
from pydantic import SecretStr
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType, NameEmail


load_dotenv()
logger = logging.getLogger(__name__)
senha_app = secret_str = SecretStr(os.getenv("MAIL_PASSWORD", ""))
MAIL_ENABLED = os.getenv("MAIL_ENABLED", "false").lower() == "true"

config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=senha_app,
    MAIL_FROM=os.getenv("MAIL_FROM", "noreply@example.com"),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "localhost"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

fm = FastMail(config)


async def enviar_confirmacao(email: str, nome: str):
    if not MAIL_ENABLED:
        return

    mensagem = MessageSchema(
        subject="Conta criada com sucesso!",
        recipients=[NameEmail(name=nome, email=email)],
        body=f"<h1>Olá, {nome}!</h1><p>É com muito prazer que informamos a confirmação de sua conta.</p>",
        subtype=MessageType.html,
    )
    try:
        await fm.send_message(mensagem)
    except Exception:
        # O cliente já foi salvo; falhas temporárias no SMTP não devem cancelar
        # o cadastro. O erro continua disponível no log do servidor.
        logger.exception("Não foi possível enviar a confirmação para %s", email)
