#!/usr/bin/python -tt
"""
Author: Mostafa Altantawy 
Email: Mostafa.Altantawy@Gmail.com
Version 0.1
"""
import imaplib, email 
from ConfigParser import ConfigParser



config = ConfigParser()
config.read('config.ini')
mail_server = config.get('server_config', 'server_hostname')
user_name = config.get('server_config', 'user_name')
password = config.get('server_config', 'password')
path = config.get('file_path', 'path')


class GetMail():
	connection = None
	error = None

	def __init__(self, mail_server, username, password):
		self.connection = imaplib.IMAP4(mail_server)
		self.connection.login(username, password)
		self.connection.select(readonly=False)


	def close_connection(self):
		self.connection.close()
		

	def download_attachments_in_email(self, connection, emailid, outputdir):
		
		response, data = self.connection.fetch(emailid, "(BODY.PEEK[])")
		email_body = data[0][1]
		mail = email.message_from_string(email_body)
		msg_id = []
		if mail.get_content_maintype() != 'multipart':
			return
		for part in mail.walk():
			msg_id.append(part['Message-ID'])
			msg_id = [elem for elem in msg_id if elem != None]
			msg_id = [elem.replace('<', '') for elem in msg_id]
			msg_id = [elem.replace('>', '') for elem in msg_id]
			if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
				for elem in msg_id:
					open(outputdir + '/' + elem + '-'+ part.get_filename(), 'wb').write(part.get_payload(decode=True))
		
	def download_all_attachments_in_inbox(self, server, user, password, outputdir):
		response, items = self.connection.search(None, "(ALL)")
		items = items[0].split()
		for emailid in items:
			self.download_attachments_in_email(self.connection, emailid, outputdir)


		

imap_connect = GetMail(mail_server, user_name, password)
imap_connect.download_all_attachments_in_inbox(mail_server, user_name, password, path)
imap_connect.close_connection()
