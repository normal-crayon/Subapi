#!/usr/bin/env python3

import imaplib, email
from email.header import decode_header
from colorama import Fore as debugColor, Style
import os
import webbrowser

class read_email:
    '''
    TODO:
    4. find a way to store emails as json 
    5. parse it to whatsapp and make a whatsapp bot
    6. real time fetching (how tho??)

    '''
    def __init__(self, username, password, email, Debug=0):
        self.username = username
        self.password = password
        self.email = email
        self.debug = Debug 

    def login(self):

        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.debug = self.debug
        self.imap.login(self.username, self.password)
        self.status, self.messages = self.imap.select("INBOX")
           


    def search(self, key, val, scope):
        result, data = self.imap.search(None, key, f'{val}', scope)
        uid = [int(s) for s in data[0].split()]
        return result, data, uid

    def obtain_header(self, msg):
        '''
        decodes email subject, from and to
        '''
        sub, encoding = decode_header(msg["Subject"])[0]
        if isinstance(sub, bytes):
            sub = sub.decode(encoding)

        From, encoding = decode_header(msg["From"])[0]
        if isinstance(From, bytes):
            From = From.decode(encoding)

        return sub, From


    def download_attachment(self, part):
        '''
        downloads any attachment in mail
        TODO: implement later 
        '''
        pass
   
    def get_body(self, msg):
        for resp in msg:
            if isinstance(resp, tuple):
                msg = email.message_from_bytes(resp[1])

                sub, From = self.obtain_header(msg)
                print("Subject: ", sub)
                print("From: ", From)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            return body, content_type


                        elif "attachment" in content_disposition:
                            self.download_attachment(part)

#                            elif content_type == "text/html":
#                                content_type = msg.get_content_type()
#                                body = msg.get_payload(decode=True).decode()
#
#                                if content_type == "text/html":
#                                    self.open_html(body, sub)
#
                        else:
                            print(content_type)


    def read_msgs(self, key="FROM", val="vitianscdc2023@vitstudent.ac.in", scope="UNSEEN", number_of_msgs=1):

        typ, [msg_list], _ = self.search(key, val, scope)

        for i, num in enumerate(msg_list.split()[::-1]):
            res, msg = self.imap.fetch(num, "(RFC822)")
            print(debugColor.GREEN + str(i))
            print(Style.RESET_ALL)
            if i == number_of_msgs:
                break
            try:
                body, content_type = self.get_body(msg)
                print(body)
            except:
                print("body is not parsing")

    def fetch_for_uid(self, uid):
        res, msg = self.imap.fetch(uid, "(RFC822)")
        print(debugColor.GREEN + str("New message!!"))
        print(Style.RESET_ALL)
        try:
            body, content_type = self.get_body(msg)
            print(body)
        except:
            print("body not parsing for uid")

            
    def open_html(self, body, sub):
        '''
        replace this with webscrapping technique to scrape content alone
        TODO:
        1. implement bueatifulsoup scrapper 
        '''
        filename = "index.html"
        filepath = os.path.join(folder_name, filename)

        open(filepath, "w").write(body)
        webbrowser.open(filepath)

    def logout(self):
        self.imap.logout()
        return 1

    def close(self):
        self.imap.close()
