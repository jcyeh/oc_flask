import smtplib
from flask import Flask
application = Flask(__name__)

port = 587
smtp_server = 'smtp-relay.sendinblue.com'
username = 'jcyeh@familyfirstnetwork.org'
password = '3fJCwD8sV1KAI2aW'

from_add = 'jcyeh@familyfirstnetwork.org'
to_add = 'jcyeh@larc.ee.nthu.edu.tw'

sender = from_add
receivers = [to_add]

message = f"""\
Subject: TEST MAIL 4
To: {to_add}
From: {from_add}

This is test mail 4!"""

@application.route("/")
def hello():
    smtpObj = smtplib.SMTP(smtp_server, port)
    smtpObj.login(username, password)
    #smtpObj.set_debuglevel(1)
    smtpObj.sendmail(sender, receivers, message)
    smtpObj.quit()

    return "TEST Mail, JC!"

if __name__ == "__main__":
    application.run()
