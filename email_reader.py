#!/usr/bin/env python3

import os
import argparse
import imaplib, email
import time 
from email_class import read_email

parser = argparse.ArgumentParser(description='Welcome to Subapi (Subash-API). A synchronous server, with api support to fetch emails from originally placements CDC emails, but confugurable.', fromfile_prefix_chars='@')

parser.add_argument('-u', '--user', type=str, help='user email id to fetch from', required=True)

parser.add_argument('-p', '--password', type=str, help='apps password of your account. for more information visit https://support.google.com/', required=True)

parser.add_argument('-e', '--email', type=str, help='the particular email address from where you want your notifications', required=True)

parser.add_argument('-d', '--debug', type=int, help='you can set imap debug level. Defaults to 0', default=0)

parser.add_argument('-s', '--scope', type=str, help='set scope to UNSEEN, SEEN. Defaults to UNSEEN', default='UNSEEN')

parser.add_argument('-t', '--timeout', type=int, help='set timeout for the server. Defualts to 3 mins', default=3)

creds = parser.parse_args()

user = creds.user
password = creds.password
email = creds.email

maxUid = 0

r = read_email(user, password, email, Debug=creds.debug)

r.login()

_, _, uid = r.search(key="FROM", val=email, scope="SEEN")
if uid:
    maxUid = max(uid)


r.logout()

if __name__ == "__main__":
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
        time.sleep(creds.timeout*60)


