#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---

Uses Python's included mailbox library to convert mail archives from
maildir [http://en.wikipedia.org/wiki/Maildir] to
mbox [http://en.wikipedia.org/wiki/Mbox] format, icluding subfolder.

See http://docs.python.org/library/mailbox.html#mailbox.Mailbox for
full documentation on this library.

---

To run, save as maildir2mbox.py and run:

$ python maildir2mbox.py [maildir_path] [mbox_filename]

[maildir_path] should be the the path to the actual maildir (containing new,
cur, tmp, and the subfolders, which are hidden directories with names like
.subfolde.subsubfolder.subsubsbfolder);

[mbox_filename] will be newly created, as well as a [mbox_filename].sbd the
directory.
"""

import mailbox
import sys
import email
import os
import shutil

def maildir2mailbox(maildirname, mboxfilename):
   """
   slightly adapted from maildir2mbox.py,
   Nathan R. Yergler, 6 June 2010
   http://yergler.net/blog/2010/06/06/batteries-included-or-maildir-to-mbox-again/

   """
   # open the existing maildir and the target mbox file
   maildir = mailbox.Maildir(maildirname, email.message_from_file)
   mbox = mailbox.mbox(mboxfilename)

   # lock the mbox
   mbox.lock()

   # iterate over messages in the maildir and add to the mbox
   for msg in maildir:
       mbox.add(msg)

   # close and unlock
   mbox.close()
   maildir.close()


dirname=sys.argv[-2]
mboxname=sys.argv[-1]
#add custom
os.remove(mboxname)

print(dirname +' -> ' +mboxname)
mboxdirname=mboxname+'.sbd'
#add custom
shutil.rmtree(mboxdirname)

maildir2mailbox(dirname,mboxname)
if not os.path.exists(mboxdirname): os.makedirs(mboxdirname)

listofdirs=[dn for dn in os.walk(dirname).next()[1] if dn not in ['new', 'cur', 'tmp']]
for curfold in listofdirs:
   curlist=[mboxname]+curfold.split('.')
   curpath=os.path.join(*[dn+'.sbd' for dn in curlist if dn])
   if not os.path.exists(curpath): os.makedirs(curpath)
   print('| ' +curfold +' -> '+curpath[:-4])
   maildir2mailbox(os.path.join(dirname,curfold),curpath[:-4])

print('Done')
