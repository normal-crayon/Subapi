#!/usr/bin/env python3

import imaplib, email
from email.header import decode_header
import os
import webbrowser
from email_class import read_email

user = 'prithviraj.2019@vitstudent.ac.in'
password = 'cvojgbhrefysoypx'

r = read_email(user, password, "vitianscdc2023@vitstudent.ac.in", Debug = 4)
_, _, uid = r.search(key="FROM", val="vitianscdc2023@vitstudent.ac.in", scope="SEEN")
r.read_msgs(scope="SEEN", number_of_msgs=10)
maxUid = max(uid)
r.close()
