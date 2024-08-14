import smtplib
import email.utils
from email.mime.text import MIMEText

class SmtpEmail():
    @classmethod
    def send_email(cls,to_email: str, subject: str, body: str):
        # Create the email content
        message = MIMEText(body)
        message["To"] = email.utils.formataddr(("Recipient", to_email))
        message["From"] = email.utils.formataddr(("Pei", "peileon2@126.com"))
        message["Subject"] = subject

        # Configure the 126 email SMTP server
        smtp_server = "smtp.126.com"
        smtp_port = 465
        username = "peileon2@126.com"
        app_password = "XDIPJLGQIHMUKTVF"

        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(True)

        try:
            # Login to the server
            server.login(username, app_password)

            # Send the email
            server.sendmail(username, [to_email], message.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            # Close the connection
            server.quit()
