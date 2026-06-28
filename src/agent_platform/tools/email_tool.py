import os

EMAIL_TOOL = {
    "name": "send_email",
    "description": "Send an email via the SMTP server",
    "input_schema": {
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["to", "subject", "body"]
    }
}


def send_email_handler(to: str, subject: str, body: str) -> str:
    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "2525"))
    try:
        import smtplib
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            msg = f"From: agent@platform.com\r\nTo: {to}\r\nSubject: {subject}\r\n\r\n{body}"
            server.sendmail("agent@platform.com", [to], msg)
        return f"Email sent to {to}"
    except Exception as e:
        return f"Email send failed: {e}"
