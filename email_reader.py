#!/usr/bin/env python3

import imaplib, email
import os
import webbrowser
import time 
from email_class import read_email
from email.header import decode_header

user = 'prithviraj.2019@vitstudent.ac.in'
password = 'cvojgbhrefysoypx'
email = "vitianscdc2023@vitstudent.ac.in"
maxUid = 0

r = read_email(user, password, email, Debug=0)

r.login()

_, _, uid = r.search(key="FROM", val=email, scope="SEEN")
if uid:
    maxUid = max(uid)


r.logout()



while True:
    r.login()

    _, _, uid = r.search(key="FROM", val=email, scope="UNSEEN")
    
    for i in uid:
        if i > maxUid:
            r.fetch_for_uid(str(i).encode())
            maxUid = i
            #print(maxUid)
    r.logout()
    print("No new messages yet...")
    time.sleep(3*60)

#
