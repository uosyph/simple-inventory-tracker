from app import app
from smtplib import SMTP
from email.mime.text import MIMEText


def send_low_stock_email(ingredient):
    # Email content
    sender = app.config["SENDER"]
    recipients = app.config["DESTINATION"]
    subject = f"{ingredient.name} is low on stock."
    body = f"""
    <html>
        <body>
            <h2>{ingredient.name} stock is less than 50%.</h2>
            <p><strong>Ingredient:</strong> {ingredient.name}</p>
            <p><strong>Current Stock:</strong> {ingredient.stock}</p>
            <p><strong>Initial Stock:</strong> {ingredient.initial_stock}</p>
        </body>
    </html>
    """

    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipients

        # Establish SMTP connection and send email
        with SMTP(app.config["SMTP_SERVER"], app.config["SMTP_PORT"]) as conn:
            conn.ehlo()
            conn.starttls()
            conn.ehlo()
            conn.login(app.config["EMAIL"], app.config["PASSWORD"])
            conn.sendmail(sender, recipients, msg.as_string())

        return True
    except Exception as e:
        return False, str(e)
