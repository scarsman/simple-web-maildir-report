# simple-web-maildir-report

Purpose:
	Reading emails in Maildir and display it in a web browser for monitoring email domains if it is detected as spammer
	Run it in crontab to constantly read mailbox
	Ex:
		`*/5 * * * * /usr/bin/python2.7 /home/forge/readmailbox/maildir2mbox.py /home/forge/Maildir/ /home/forge/readmailbox/mailbox.box`
		`*/10 * * * * /usr/bin/python2.7 /home/forge/readmailbox/readmailbox.py /home/forge/readmailbox/mailbox.box /home/forge/readmailbox/mailbox.json`