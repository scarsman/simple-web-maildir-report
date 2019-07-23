import mailbox
import email
import ujson
import quopri
import json

from BeautifulSoup import BeautifulSoup

import json
from datetime import datetime,timedelta

import os
import sys

MBOX = '/home/forge/readmailbox/mailbox.box'
OUT_FILE = '/home/forge/readmailbox/mailbox.json'

#os.remove(OUT_FILE)
#print("File Removed!")

class Encoder(json.JSONEncoder):
    def default(self, o): return  list(o)

def clean_content(msg):

    msg = quopri.decodestring(msg)

    try:
        soup = BeautifulSoup(msg)
    except:
        return ''

    return ''.join(soup.findAll(text=True))

def extract_body_content(msg):

    payload = msg.get_payload()

    content = ''

    if msg.is_multipart():
        for sub_msg in payload:
            content = extract_body_content(sub_msg)
    else:
        content = payload

    return content

def objectify_message(msg):

    # Map in fields from the message
    o_msg = dict([ (k, v) for (k,v) in msg.items() ])
    part = [p for p in msg.walk()][0]
    o_msg['contentType'] = part.get_content_type()
    o_msg['content'] = clean_content(extract_body_content(part))

    return o_msg

def get_json_messages(mb):

    while 1:
        msg = mb.next()

        if msg is None: break

        #messages.append(objectify_message(msg))
        yield objectify_message(msg)
    #print ujson.dumps(messages, indent=4)
    #return messages


def dt_parse(t):
    ret = datetime.strptime(t[0:25],"%a, %d %b %Y %H:%M:%S")

    if t[26]=='+':
        ret -=timedelta(hours=int(t[27:29]))
    elif t[26]=='-':
        ret +=timedelta(hours=int(t[27:29]))

    return ret


if len(sys.argv) != 3:
    print("Usage: {0} </path/to/readmailbox.py>".format(__file__))
    sys.exit(1)

MBOX = sys.argv[1]
OUT_FILE = sys.argv[2]

mbox = mailbox.UnixMailbox(open(MBOX, 'rb'), email.message_from_file)
messages = []

with open(OUT_FILE , 'w') as outfile:

    for msg in get_json_messages(mbox):
        if msg != None:
            messages.append(msg)

    data_sorted = sorted(messages, key = lambda k: dt_parse(k["Date"]),reverse=True)

    json.dump(data_sorted, outfile)

    print "Done"

