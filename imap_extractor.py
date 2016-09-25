#!/usr/bin/python -tt
"""
Author: Mostafa Altantawy 
Email: Mostafa.Altantawy@Gmail.com
version 0.2
"""
import imaplib, email, re
from ConfigParser import ConfigParser



config = ConfigParser()
config.read('config.ini')
mail_server = config.get('server_config', 'server_hostname')
user_name = config.get('server_config', 'user_name')
password = config.get('server_config', 'password')
files_path = config.get('path', 'files_path')
urls_path = config.get('path', 'urls_path') 


class GetEmail():
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

	def extract_url(self):
		urls_dict = dict()
		response, items = self.connection.search(None, "(ALL)")
		items = items[0].split()
		for emailid in items:
			response, data = self.connection.fetch(emailid, "(BODY.PEEK[])")
			email_body = data[0][1]
			mail = email.message_from_string(email_body)
			for part in mail.walk():
				if re.findall(r'(https?://\S+)', str(part)):
					urls_dict[part['Message-ID']] = re.findall(r'(https?://\S+)', str(part))
		for k, v in urls_dict.items():
			urls_dict[k] = ''.join(v)
		
		urls =  open(str(urls_path) + '/' + 'urls.txt', 'w')
		for k, v in sorted(urls_dict.items()):
			urls.write(str(k) +','+str(v) + '\n')
		urls.close()


		

imap_connect = GetEmail(mail_server, user_name, password)
imap_connect.extract_url()
imap_connect.download_all_attachments_in_inbox(mail_server, user_name, password, files_path)
imap_connect.close_connection()
