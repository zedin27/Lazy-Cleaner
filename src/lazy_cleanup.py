"""Email parser in a folder/labels with Gmail currently."""

from email.parser import HeaderParser
from imapclient import IMAPClient
import imaplib, email
import sys

user = 'buying_gf@runescape.lol'
pw = 'no u'
imap_url = 'your.domain.edu/com/org/whatever'

def auth(user, pw):
	"""Authentication via IMAPClient.

	:param user: Login username.
	:param pw: Password.
	:returns: Authorization to the connection/server.
	"""
	server = IMAPClient(imap_url)
	try:
		server.login(user, pw)
	except imaplib.IMAP4.error:
		print ("LOGIN FAILED!!! ")
		sys.exit(1)
	return (server)

def auth_imap4_ssl(user, pw, imap_url):
	"""Authentication via IMAPC_SSL.

	:param user: Login username.
	:param pw: Password.
	:returns: Authorization to the connection/server.
	"""
	server = imaplib.IMAP4_SSL(imap_url)
	try:
		server.login(user, pw)
	except imaplib.IMAP4.error:
		print ("LOGIN FAILED!!! ")
		sys.exit(1)
	return (server)

def get_body(msg):
	"""Extract email content."""

	if msg.is_multipart():
		return get_body(msg.get_payload(0))
	else:
		return msg.get_payload(None, True)

def search(key, value):
	"""Search criterias (list on search_criteria.txt)."""

	server = auth(user, pw)
	result, data = server.search(None, key,'"{}"'.format(value))
	return (data)

def get_emails(result_bytes):
	"""Fetch list of emails."""

	msgs = []
	for num in result_bytes[0].split():
		typ, data = con.fetch(num, '(RFC822)')
		msgs.append(data)
	return (msgs)

def print_total_emails(mailbox=None):
	"""Print total emails from an inbox.

	:param mailbox: Folder/label/mailbox to iterate through.
	"""
	if mailbox is None:
		print("Provide with the correct mailbox/folder/label that you want to delete from.")
		sys.exit(1)
	server = auth(user, pw)
	typ, data = server.select('"{}"'.format(mailbox), readonly=True)
	print(typ, data)
	num_msgs = int(data[0])
	print("There are {0} messages in {1}".format(num_msgs, mailbox))

def print_unseen_emails(mailbox=None, search_criteria):
	"""Print total of unseen or unread emails from an inbox.

	:param mailbox: Folder/label/mailbox to iterate through.
	:param search_criteria: Delimeters or specifications to search for.
	"""
	if search_criteria.find("UNSEEN") is 0:
		print("search_criteria is 'UNSEEN' while it is setup by default.")
		sys.exit(1)
	if mailbox is None:
		print("Provide with the correct mailbox/folder/label that you want to delete from.")
		sys.exit(1)
	server = auth(user, pw)
	server.select_folder('{}'.format(mailbox), readonly=True)
	messages = server.search('UNSEEN {}'.format(search_criteria))
	unseen = 0
	for uid, message_data in server.fetch(messages, 'RFC822').items():
		email_message = email.message_from_bytes(message_data[b'RFC822'])
		unseen += 1
	print("Search criteria ({0}) with {1} unread messages on your user ({2}).".format(search_criteria, unseen, user))

def nuke_emails(mailbox=None):
	"""Sends ALL emails from a desired inbox to Trash folder.

	:param mailbox: Folder/label/mailbox to iterate through.
	"""
	if mailbox is None:
		print("Provide with the correct mailbox/folder/label that you want to delete from.")
		sys.exit(1)
	server = auth_imap4_ssl(user, pw, imap_url)
	server.select('{}'.format(mailbox))
	typ, data = server.search(None, 'ALL')
	total_msgs = 0
	print("Deleting all from {0}...".format(mailbox))
	for msg_num in data[0].split():
		server.store(msg_num, '+X-GM-LABELS', '\\Trash')
		total_msgs += 1
	print("{0} total amount of emails are sent to Trash".format(total_msgs))

if __name__ == '__main__':
	server = auth(user, pw)
	# print_unseen_emails('INBOX', 'TO "CSUMB" SUBJECT "Why"')
	# nuke_emails('INBOX')
	server.logout()
