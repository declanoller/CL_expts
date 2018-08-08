import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import imaplib



class EmailTools:

    def __init__(self,debug_file):
        self.info = {}
        self.server = None
        self.debug_file = debug_file
        with open("addresses_info.txt") as f:
            for line in f:
                (key, val) = line.split()
                self.info[key] = val
                #print(key,': ',val)

        '''self.port = 587
        print('starting email server and logging in...')
        self.server = smtplib.SMTP('smtp.gmail.com', self.port)
        self.server.starttls()
        self.server.login(self.info['sender_email'], self.info['sender_password'])
        print('done')'''


    def getUnreadEmails(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.info['sender_email'], self.info['sender_password'])
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox") # connect to inbox.

        result, data = mail.search(None, "ALL")

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest

        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

        raw_email = data[0][1] # here's the body, which is raw text of the whole email
        # including headers and alternate payloads



    def sendEmailOffer(self, post, price_offered, msg_type):

        msg = self.createEmailMessage(post, price_offered, msg_type)

        self.debug_file.writeToDebug('\nemail to be sent:')
        self.debug_file.writeToDebug(msg.as_string())

        '''print('\nemail to be sent:')
        print(msg.as_string())'''

        print('\npretend sending email!')

        return(msg['In-Reply-To'])

        self.debug_file.writeToDebug('sending email')
        self.server.send_message(msg)


    def createEmailMessage(self, post, price_offered, msg_type):

        if msg_type=='polite':
            msg_file = 'polite_message.txt'
            with open(msg_file) as f:
                content = f.read()
            content_filled = content.format(price_offered,post.page)

        if msg_type=='available':
            msg_file = 'is_available_message.txt'
            with open(msg_file) as f:
                content = f.read()
            content_filled = content.format(post.page)


        msg = EmailMessage()
        msg['Subject'] = post.title
        msg['From'] = self.info['sender_email']
        msg['To'] = post.email

        msg.set_content(content_filled)

        my_id = make_msgid()
        msg['In-Reply-To'] = my_id
        msg['References'] = my_id

        return(msg)







    def __del__(self):
        if self.server is not None:
            self.debug_file.writeToDebug('quitting smtp email server via ET __del__')
            print('quitting smtp email server via ET __del__')
            self.server.quit()



    def otherstuff(self):
        my_id = make_msgid()
        print('my id:',my_id)

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(info['sender_email'], info['sender_password'])


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

        #self.server.sendmail(info['sender_email'], info['recipient_email'], msg)
        self.server.send_message(msg)
        self.server.quit()



#
