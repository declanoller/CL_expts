import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

my_id = make_msgid()
print('my id:',my_id)
info = {}
with open("addresses_info.txt") as f:
    for line in f:
       (key, val) = line.split()
       info[key] = val
       print(key,': ',val)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(info['sender_email'], info['sender_password'])


content = 'email numero tres!'
#my_id = '<153365985111.3144.10898008056301223644@TITTYWHISKERS88>'
msg = EmailMessage()
msg["Message-ID"]  = my_id
msg['Subject'] = 'Testing threads'
msg['From'] = info['sender_email']
msg['To'] = info['recipient_email']
msg.set_content(content)

msg["In-Reply-To"] = my_id
msg["References"] = my_id

#server.sendmail(info['sender_email'], info['recipient_email'], msg)
server.send_message(msg)
server.quit()
