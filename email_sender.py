"""
utils/email_sender.py
Módulo reutilizable para envío de correos via Office 365 SMTP.

CONFIGURACION (GitHub Secrets):
    SMTP_EMAIL    = DiegoMaldonado@insurtechpr.com
    SMTP_PASSWORD = tu_app_password_de_office365

USO:
    from utils.email_sender import send_email

    send_email(
        to="destinatario@email.com",
        subject="Asunto del correo",
        html_body="<h1>Contenido HTML</h1>"
    )
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ─────────────────────────────────────────
# CONFIGURACION — viene de GitHub Secrets
# ─────────────────────────────────────────
SMTP_SERVER   = "smtp.office365.com"
SMTP_PORT     = 587
SMTP_EMAIL    = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")


def send_email(to: str, subject: str, html_body: str) -> None:
    """
    Envía un correo HTML via Office 365 SMTP.

    Args:
        to:        Dirección de destino, ej. "DiegoMaldonado@insurtechpr.com"
        subject:   Asunto del correo
        html_body: Contenido en formato HTML

    Raises:
        ValueError: Si faltan las credenciales SMTP
        Exception:  Si falla el envío
    """
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise ValueError(
            "Faltan credenciales SMTP. "
            "Configura SMTP_EMAIL y SMTP_PASSWORD en GitHub Secrets."
        )

    msg = MIMEMultipart("alternative")
    msg["From"]    = SMTP_EMAIL
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(msg)

    print(f"  Correo enviado exitosamente via Office 365 SMTP ✓")
    print(f"  De:   {SMTP_EMAIL}")
    print(f"  Para: {to}")
