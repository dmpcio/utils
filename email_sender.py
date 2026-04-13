"""
utils/email_sender.py
Módulo reutilizable para envío de correos via Microsoft Graph API.

CONFIGURACION (GitHub Secrets):
    AZURE_CLIENT_ID     = Application (client) ID de Azure
    AZURE_TENANT_ID     = Directory (tenant) ID de Azure
    AZURE_CLIENT_SECRET = Client secret de Azure

USO:
    from utils.email_sender import send_email

    send_email(
        to="destinatario@email.com",
        subject="Asunto del correo",
        html_body="<h1>Contenido HTML</h1>"
    )
"""

import os
import requests

# ─────────────────────────────────────────
# CONFIGURACION — viene de GitHub Secrets
# ─────────────────────────────────────────
CLIENT_ID     = os.environ.get("AZURE_CLIENT_ID", "")
TENANT_ID     = os.environ.get("AZURE_TENANT_ID", "")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")
SENDER_EMAIL  = "DiegoMaldonado@insurtechpr.com"


def get_access_token() -> str:
    """
    Obtiene un access token de Microsoft Graph via Client Credentials.
    """
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type":    "client_credentials",
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope":         "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Error obteniendo token: {response.status_code} {response.text}")
    return response.json()["access_token"]


def send_email(to: str, subject: str, html_body: str) -> None:
    """
    Envía un correo HTML via Microsoft Graph API.

    Args:
        to:        Dirección de destino
        subject:   Asunto del correo
        html_body: Contenido en formato HTML

    Raises:
        ValueError: Si faltan las credenciales de Azure
        Exception:  Si falla el envío
    """
    if not CLIENT_ID or not TENANT_ID or not CLIENT_SECRET:
        raise ValueError(
            "Faltan credenciales de Azure. "
            "Configura AZURE_CLIENT_ID, AZURE_TENANT_ID y AZURE_CLIENT_SECRET "
            "en GitHub Secrets."
        )

    token = get_access_token()

    url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"

    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 202:
        print(f"  Correo enviado exitosamente via Microsoft Graph ✓")
        print(f"  De:   {SENDER_EMAIL}")
        print(f"  Para: {to}")
    else:
        raise Exception(
            f"Error enviando correo: {response.status_code} {response.text}"
        )
