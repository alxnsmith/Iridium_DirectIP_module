import os
import smtplib
import ssl
from configparser import ConfigParser
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename


class Mail:
    class SMTP:
        """
        SMTP class
        """

        def __init__(self, host: str, port: int, username: str, password: str):
            """
            SMTP class constructor
            """
            self.host = host
            self.port = port
            self.username = username
            self.password = password

        def send_mail(
            self,
                subject: str,
                message: str,
                from_email: str,
                recipient_list: list,
                fail_silently: bool = False,
        ):
            """
            Pure send_mail python function
            Use smtplib
            """
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = ", ".join(recipient_list)
            ssl_context = ssl.create_default_context()
            # attach file to mail 300234064010960_001105.sbd

            try:
                with smtplib.SMTP_SSL(self.host, self.port, context=ssl_context) as server:
                    server.login(self.username, self.password)
                    server.sendmail(from_email, recipient_list,
                                    msg.as_string())
            except Exception as e:
                if fail_silently:
                    return False
                raise e

            return True

        def send(self, msg: 'Mail.Message', fail_silently: bool = False):
            ssl_context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(self.host, self.port, context=ssl_context) as server:
                    server.login(self.username, self.password)
                    server.sendmail(msg.from_email, msg.recipients,
                                    msg.make().as_string())
            except Exception as e:
                if fail_silently:
                    return False
                raise e

            return True

    class Message:
        def __init__(self, subject: str, message: str, from_email: str, recipients: list, attachments: list = []):
            self.subject = subject
            self.message = message
            self.from_email = from_email
            self.recipients = recipients
            self.attachments = attachments

        def attach_file(self, filename):
            self.attachments.append(filename)

        def make(self):
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.recipients)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = self.subject

            msg.attach(MIMEText(self.message))
            for f in self.attachments or []:
                filename = basename(f)
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=filename)

                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % filename
                msg.attach(part)

            return msg

    class Config:
        def __init__(self, host: str, port: int, username: str, password: str, recipients: list):
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            self.recipients = recipients

    @staticmethod
    def parse_config(config_file: str) -> Config:
        # read config
        config = ConfigParser()
        config.read(config_file)
        # get config
        host = config.get('SMTP', 'host')
        port = config.getint('SMTP', 'port')
        login = config.get('SMTP', 'login')
        password = config.get('SMTP', 'password')
        recepients = config.get('SMTP', 'recepients').split(', ')

        return Mail.Config(host, port, login, password, recepients)

    @staticmethod
    def send_message(imei: str, payload: bytes, config: Config):
        # if tmp dir is not exists - create it
        if not os.path.exists('temp'):
            os.makedirs('temp')
        attachment = f'temp/{imei}.sbd'
        # create file with payload in tmp dir
        with open(attachment, 'wb') as f:
            f.write(payload)

        # Make message object with attachment file and imei as subject
        msg = Mail.Message(subject=imei, message='', from_email=config.username,
                           recipients=config.recipients, attachments=[attachment])

        # Send message
        smtp = Mail.SMTP(host=config.host, port=config.port,
                         username=config.username, password=config.password)
        smtp.send(msg)

        # remove file from tmp dir
        os.remove(attachment)


if __name__ == "__main__":
    config = Mail.parse_config('config.ini')
    Mail.send_message('300234064010960', b'hello', config)
