from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from news.settings import env


@shared_task
def send_email(message_to, subject, text):
    message = Mail(
        from_email='logotip123@yahoo.com',
        to_emails=message_to,
        subject=subject,
        html_content=text)
    sg = SendGridAPIClient(env.str('SENDGRID_API_KEY'))
    sg.send(message)
    return None
