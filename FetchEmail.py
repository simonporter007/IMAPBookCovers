from datetime import datetime, timedelta
import email
import imaplib
import os

class FetchEmail():

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False) # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachment(self, msg, download_folder="/mnt/us/documents"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = False
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename().replace(' ', '-')
            filename = ''.join(filename.splitlines())
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path

    def fetch_unread_messages_with_attachments_since(self, since_days=1):
        """
        Retrieve unread messages
        """
        emails = []
        since_date = (datetime.now() - timedelta(days=since_days)).strftime( "%d-%b-%Y" )
        (result, messages) = self.connection.search(None, 'SINCE', since_date, 'UnSeen')
        if result == "OK":
            for message in messages[0].split(' '):
                try: 
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    self.close_connection()
                    exit()
                    
                msg = email.message_from_string(data[0][1])

                if msg.get_content_maintype() != 'multipart':
                    continue

                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')

            return emails

        self.error = "Failed to retreive emails."
        return emails