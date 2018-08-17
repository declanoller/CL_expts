import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import imaplib
import email




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

    def startSMTP(self):
        #For writing emails.
        self.port = 587
        print('starting email server and logging in...')
        self.debug_file.writeToDebug('starting email server on port {} and logging in...'.format(self.port))
        self.server = smtplib.SMTP('smtp.gmail.com', self.port)
        self.server.starttls()
        self.server.login(self.info['sender_email'], self.info['sender_password'])
        self.debug_file.writeToDebug('successful!')
        print('done')


    def getUnreadEmails(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.info['sender_email'], self.info['sender_password'])
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox") # connect to inbox.

        result, data = mail.search(None, '(UNSEEN)')

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        #print(id_list)
        #latest_email_id = id_list[-1] # get the latest
        mail_list = []
        for id in id_list:
            result, data = mail.fetch(id, '(RFC822)') # fetch the email body (RFC822) for the given ID
            #print('\n\nraw email:')
            raw_email = data[0][1] # here's the body, which is raw text of the whole email
            msg = email.message_from_bytes(raw_email)
            mail_list.append(msg)
            #print('keys:',msg.keys())

        mail.logout()

        return(mail_list)



    def sendEmailOffer(self, post, price_offered, msg_type):
        if self.server is None:
            self.startSMTP()

        msg = self.createEmailMessage(post, price_offered, msg_type)

        self.debug_file.writeToDebug('email to be sent:\n' + msg.as_string() + '\n\n')

        self.debug_file.writeToDebug('sending email\n')
        self.server.send_message(msg)
        return(msg['In-Reply-To'])


    def sendCancelEmail(self,post):
        if self.server is None:
            self.startSMTP()

        msg = self.createEmailMessage(post, 0, 'cancel')

        #Need to use the same id thing as before
        #I'm not totally sure about the difference between these two fields...
        msg['In-Reply-To'] = post.email_id
        msg['References'] = post.email_id

        self.debug_file.writeToDebug('email to be sent:\n' + msg.as_string() + '\n\n')

        self.debug_file.writeToDebug('sending email\n')
        self.server.send_message(msg)
        return(msg['In-Reply-To'])



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

        if msg_type=='cancel':
            msg_file = 'cancel_message.txt'
            with open(msg_file) as f:
                content = f.read()
            content_filled = content.format(post.page)


        msg = EmailMessage()
        msg['Subject'] = post.title
        msg['From'] = self.info['sender_email']
        msg['To'] = post.email
        #msg['To'] = self.info['recipient_email']

        msg.set_content(content_filled)

        my_id = make_msgid()
        msg['In-Reply-To'] = my_id
        msg['References'] = my_id

        return(msg)







    def __del__(self):
        if self.server is not None:
            #self.debug_file.writeToDebug('quitting smtp email server via ET __del__')
            print('quitting smtp email server via ET __del__')
            self.server.quit()






#
