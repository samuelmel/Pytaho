import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
import httpx
from src.utils.logger import logger
"""
notifications.py - Alertas e Notificações (Slack, Teams, E-mail).
Equivalente ao Job Entry 'Mail' do Pentaho Kettle.
"""

class NotificationService:
    """
    Equivalente ao Job Entry 'Mail' do Pentaho.
    Envia alertas de sucesso/falha via Webhook (Slack/Teams) ou E-mail (SMTP).
    """

    @staticmethod
    def send_slack(message: str, webhook_url: Optional[str] = None) -> bool:
        """Envia mensagem via webhook para canal do Slack."""
        url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        if not url:
            logger.warning("SLACK_WEBHOOK_URL não configurada.")
            return False

        try:
            resp = httpx.post(url, json={"text": message}, timeout=10.0)
            resp.raise_for_status()
            logger.info("Notificação Slack enviada com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar notificação Slack: {e}")
            return False

    @staticmethod
    def send_teams(title: str, text: str, webhook_url: Optional[str] = None) -> bool:
        """Envia mensagem no Microsoft Teams (MessageCard format)."""
        url = webhook_url or os.getenv("TEAMS_WEBHOOK_URL")
        if not url:
            logger.warning("TEAMS_WEBHOOK_URL não configurada.")
            return False

        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": title,
            "themeColor": "0076D7",
            "title": title,
            "text": text,
        }
        try:
            resp = httpx.post(url, json=payload, timeout=10.0)
            resp.raise_for_status()
            logger.info("Notificação Teams enviada com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar notificação Teams: {e}")
            return False

    @staticmethod
    def send_email(
        subject: str,
        body_html: str,
        recipients: Optional[List[str]] = None
    ) -> bool:
        """Envia e-mail via servidor SMTP com suporte a HTML."""
        smtp_host = os.getenv("EMAIL_SMTP_HOST")
        smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        smtp_user = os.getenv("EMAIL_USER")
        smtp_pass = os.getenv("EMAIL_PASSWORD")
        to_list = recipients or os.getenv("EMAIL_ALERT_RECIPIENTS", "").split(",")

        if not (smtp_host and smtp_user and smtp_pass and to_list):
            logger.warning("Credenciais de e-mail incompletas no .env.")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = ", ".join(to_list)
            msg.attach(MIMEText(body_html, "html"))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, to_list, msg.as_string())

            logger.info("E-mail de alerta enviado com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar e-mail: {e}")
            return False

    """Disparo de alertas e notificações em caso de sucesso ou falha nas pipelines."""
    pass
