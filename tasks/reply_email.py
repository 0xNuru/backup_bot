#!/usr/bin/env python3

import json

from jinja2 import Environment, PackageLoader, select_autoescape
from robocorp import vault
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient



jinja2_env = Environment(
    loader=PackageLoader("devdata"),
    autoescape=select_autoescape(['html', 'xml'])
)

def reply_email(text: str, summary: json, to_email: str, subject: str):
    sendgrid_vault = vault.get_secret("SendGrid")
    sg_client = SendGridAPIClient(sendgrid_vault["SENDGRID_API_KEY"])
    from_email = sendgrid_vault["FROM_EMAIL"]
    template = jinja2_env.get_template("email.html")
    summary = json.loads(summary)
    html = template.render(text=text, summary=summary)
    mail = Mail(from_email=from_email,
                to_emails=to_email,
                subject="Re: " + subject,
                html_content=html
                )
    
    try:
        response = sg_client.send(mail)
    except Exception as e:
        print(f"Error sending mail: {e}")