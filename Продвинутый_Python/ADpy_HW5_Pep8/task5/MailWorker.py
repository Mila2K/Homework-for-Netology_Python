import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailWorker:
    def __init__(self, login, password, smtp_server, smtp_port_number, imap_port_number, imap_server):
        self.imap_port_number = imap_port_number
        self.imap_server = imap_server
        self.smtp_port_number = smtp_port_number
        self.smtp_server = smtp_server
        self.login = login
        self.password = password

    def send_mail(self, recipient_list, subject, body_message):
        msg = MIMEMultipart()
        msg['From'] = self.login
        receivers = ', '.join(recipient_list)
        msg['To'] = receivers
        msg['Subject'] = subject
        msg.attach(MIMEText(body_message))
        mail_sender = smtplib.SMTP(self.smtp_server, 587)
        mail_sender.ehlo()  # identify ourselves to smtp client
        mail_sender.starttls()  # secure our email with tls encryption
        mail_sender.ehlo()  # re-identify ourselves as an encrypted connection
        mail_sender.login(self.login, self.password)
        mail_sender.sendmail(self.login, receivers, msg.as_string())
        mail_sender.quit()

    def get_mail(self):
        header = None
        mail_receiver = imaplib.IMAP4_SSL(self.imap_server, self.imap_port_number)
        mail_receiver.login(self.login, self.password)
        mail_receiver.list()
        mail_receiver.select("inbox")
        search_criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        data = mail_receiver.uid('search', None, search_criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        data = mail_receiver.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail_receiver.logout()
        print(email_message)
