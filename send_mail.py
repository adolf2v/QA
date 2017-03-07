#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

# python 2.3.*: email.Utils email.Encoders
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os


# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, text2, files=[]):
    assert type(server) == dict
    assert type(to) == list
    # assert type(files) == list
    msg2 = MIMEText(text, _charset='UTF-8')
    msg = MIMEMultipart()
    msg.set_charset('UTF-8')
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    # MIMEText('中文', _charset='UTF-8')
    msgtext = MIMEText("""%s""" % text2, 'html', 'UTF-8')
    msg.attach(msgtext)
    msg.attach(msg2)

    for file in files:
        part = MIMEBase('application', 'multipart/mixed')  # 'octet-stream': binary data
        part.set_payload(text2)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)
    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()
    print 'send over'


if __name__ == "__main__":
    server = {'name': 'smtp.163.com', 'user': 'xxxxxxxxx@163.com', 'passwd': 'xxxxxx'}
    send_mail(server, 'xxxxxxxxxx@163.com', ['xxxxxx@xxxxxx.com'], 'nihao', u'gdsdsfg')
