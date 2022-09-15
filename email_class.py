#!/usr/bin/env python3

import imaplib, email
from email.header import decode_header
from colorama import Fore as debugColor, Style
import os
import webbrowser

class read_email:
    '''
    TODO:
    1. fetch and read normal text emails
    2. fetch and read html emails
    3. find a way to convert html emails to text
    4. find a way to store emails as json 
    5. parse it to whatsapp and make a whatsapp bot
    6. real time fetching (how tho??)

    '''
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.debug = 4
        self.imap.login(self.username, self.password)
        self.status, self.messages = self.imap.select("INBOX")
        
        self.numOfMsgs = int(self.messages[0])
        print(self.numOfMsgs)

    def search(self, key, val, scope):
        result, data = self.imap.search(None, key, f'{val}', scope)
        return result, data

    def obtain_header(self, msg):
        '''
        decodes email subject, from and to
        '''
        sub, encoding = decode_header(msg["Subject"])[0]
        if isinstance(sub, bytes):
            sub = sub.decode(encoding)

        From, encoding = decode_header(msg.get("From"))[0]
        if isinstance(From, bytes):
            From = From.decode(encoding)

        print("Subject: ", sub)
        print("From: ", From)

        return sub, From


    def download_attachment(self, part):
        '''
        downloads any attachment in mail
        TODO: implement later 
        '''
        pass
    
    def read_msgs(self, key="FROM", val="vitianscdc2023@vitstudent.ac.in", scope="UNSEEN"):
        typ, [msg_list] = self.search(key, val, scope)

        for i, num in enumerate(msg_list.split()[::-1]):
            res, msg = self.imap.fetch(num, "(RFC822)")
            print(debugColor.GREEN + str(i))
            print(Style.RESET_ALL)
            if i == 1:
                break
            for resp in msg:
                if isinstance(resp, tuple):
                    msg = email.message_from_bytes(resp[1])

                    sub, From = self.obtain_header(msg)

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(body)

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

