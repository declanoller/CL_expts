import pandas as pd
from datetime import datetime
import subprocess
from os import path
import numpy as np
from tabulate import tabulate
import pytz
import quopri
import re
from ScrapingTools import ScrapingTools,Post


class DatabaseTools:


    def __init__(self,debug_file):

        self.debug_file = debug_file

        self.csv_fname = 'DB_CL.csv'
        self.backup_dir = 'db_backups'
        self.csv_exists = path.exists(self.csv_fname)

        #Here, email_id is the same field as References in the email object.
        #It's what we assign in the first email that we can keep track of to keep it in the same thread.

        self.csv_fields = [
        'link',
        'post_ID',
        'email',
        'email_id',
        'title',
        'price',
        'item_type',
        'prcnt_offd',
        'price_offd',
        'replied',
        'date_cntctd',
        'date_rplied',
        'location',
        'msg_type',
        'available',
        'reply_email_id',
        'counter_offer',
        'notes',
        'phone_num'
        ]

        #Check if CSV pandas file exists, if not, create one

        if not self.csv_exists:
            self.debug_file.writeToDebug('No pandas csv file, creating one.')
            print('No pandas csv file, creating one.')
            csv_file = open(self.csv_fname,'w+')
            csv_file.write('\t'.join(self.csv_fields))
            csv_file.close()
            self.csv_exists = True
        else:
            base_name = self.csv_fname.split('.')[0]
            backup_fname = base_name + '_' + self.getDateTimeStr() + '_backup' + '.csv'
            self.debug_file.writeToDebug('Creating backup file. Backup file name:' + backup_fname)
            print('Creating backup file. Backup file name:',backup_fname)
            subprocess.check_call(['cp',self.csv_fname,self.backup_dir+'/'+backup_fname])

        self.east_tz = pytz.timezone('US/Eastern')




    def addToDatabase(self,post,email_id,percent_offered,price_offered,msg_type,location):

        self.readCSV()

        add_df = pd.DataFrame({
        'link' : [post.page],
        'post_ID' : [post.id],
        'email' : [post.email],
        'email_id' : [email_id],
        'title' : [post.title],
        'price' : [post.price],
        'item_type' : [post.post_type],
        'prcnt_offd' : [percent_offered],
        'price_offd' : [price_offered],
        'replied' : [0],
        'date_cntctd' : [self.getDateTimeStr()],
        'date_rplied' : [np.nan],
        'location' : [location],
        'msg_type' : [msg_type],
        'available' : [np.nan],
        'reply_email_id' : [np.nan],
        'counter_offer' : [np.nan],
        'notes' : [np.nan],
        'phone_num' : [post.phone_num]
        })

        self.df = self.df.append(add_df,ignore_index=True)
        self.debug_file.writeToDebug('adding to df and writing to file')
        #print('adding to df and writing to file')
        #print(self.df.head())
        self.writeCSV()







    def updateWithReply(self,reply_email):

        self.debug_file.writeToDebug('\n\nHandling reply email:')
        self.debug_file.writeToDebug('\n{}'.format(reply_email))

        print('\n\nHandling reply email:')
        print('\n{}'.format(reply_email))

        send_cancel_email = False
        self.readCSV()

        if self.shouldUpdateDB(reply_email):

            self.debug_file.writeToDebug('Email reference in DB, updating.')

            #Get date in right format
            dt_obj = datetime.strptime(reply_email['Date'],"%a, %d %b %Y %H:%M:%S %z").astimezone(self.east_tz)
            dt_string = dt_obj.strftime("%Y-%m-%d_%H-%M-%S")

            #Update the DB with the things we can
            self.df.loc[self.df['email_id']==orig_ref,'date_rplied'] = dt_string
            self.df.loc[self.df['email_id']==orig_ref,'replied'] = 1
            self.df.loc[self.df['email_id']==orig_ref,'reply_email_id'] = reply_email['Message-ID']

            main_msg = self.getMainMessage(reply_email)
            num_found = self.getNumbersInString(main_msg)
            send_cancel_email = self.handleMainMessage(num_found,main_msg)

            self.debug_file.writeToDebug('Reply main message:')
            self.debug_file.writeToDebug('\n{}'.format(main_msg))

            self.debug_file.writeToDebug('\nnum found in message: {}'.format(num_found))

            self.writeCSV()

        return(send_cancel_email)





    def readCSV(self):
        self.df = pd.read_csv(self.csv_fname,delimiter='\t')


    def writeCSV(self):
        self.df.to_csv(self.csv_fname,sep="\t",index=False)


    def getDateTimeStr(self):
        dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return(dt_string)


    def getPostFromEmail(self,email):

        ID = email['References']

        p = Post(self.df.loc[self.df['email_id']==ID,'link'].values[0])
        p.email = self.df.loc[self.df['email_id']==ID,'email'].values[0]
        p.title = self.df.loc[self.df['email_id']==ID,'title'].values[0]
        p.email_id = ID

        return(p)


    def isDuplicate(self,post):

        dupe = False

        if (post.phone_num is not None) and (len(self.df.loc[self.df['phone_num']==post.phone_num].values)!=0):
            dupe = True
            self.debug_file.writeToDebug('Phone number already in DB, duplicate: {}'.format(self.df.loc[self.df['phone_num']==post.phone_num].values.tolist()))
        if len(self.df.loc[self.df['title']==post.title].values)!=0:
            dupe = True
            self.debug_file.writeToDebug('Post title already in DB, duplicate: {}'.format(self.df.loc[self.df['title']==post.title].values.tolist()))



        return(dupe)


    def shouldUpdateDB(self,reply_email):

        reply = False

        #Only reply if the references field has an entry.
        if reply_email['References'] is not None:
            ref_list = reply_email['References'].split()
            orig_ref = [id for id in ref_list if 'TITTYWHISKERS88' in id]
            if orig_ref!=[]:
                orig_ref = orig_ref[0]
                #Check if this email is actually responding to one in the DB, and that it hasn't been responded to yet
                if (orig_ref in self.df['email_id'].values) and (self.df.loc[self.df['email_id']==orig_ref,'reply_email_id'].values[0].isnull()):
                    reply = True

        return(reply)


    def getMainMessage(self,email):

        #If it's multipart, you have to combine them.
        if email.is_multipart():
            body = ''
            for payload in email.get_payload():
                # if payload.is_multipart(): ...
                body = body + payload.get_payload()
        else:
            body = email.get_payload()

        body_parts = body.split('\n>')
        main_msg = body_parts[0]
        main_msg = quopri.decodestring(main_msg).decode('utf-8')

        return(main_msg)



    def getNumbersInString(self,string):
        num_found = re.findall(r'\d+', string)
        num_found = list(map(int,num_found))
        return(num_found)


    def handleMainMessage(self,num_found,main_msg):

        send_cancel_email = False

        #Did they accept or not?
        if len(num_found)>0:
            if len(num_found)==1:
                #This will assume that if there's one number in there, it's probably their counter offer.
                counter_offer = num_found[0]

                orig_price = self.df.loc[self.df['email_id']==orig_ref,'price'].values[0]
                orig_offer = self.df.loc[self.df['email_id']==orig_ref,'price_offd'].values[0]

                self.debug_file.writeToDebug('Only one num found: {}'.format(counter_offer))

                if counter_offer<=orig_price and counter_offer>=orig_offer:
                    self.df.loc[self.df['email_id']==orig_ref,'counter_offer'] = counter_offer
                    self.df.loc[self.df['email_id']==orig_ref,'available'] = 1
                    self.debug_file.writeToDebug('offer within expected bds: {}<={}<={}'.format(orig_offer,counter_offer,orig_price))
                else:
                    #This will be if the number in the msg in out of the bounds we expect, in which case keep track of that
                    #but don't record it as an offer.
                    self.df.loc[self.df['email_id']==orig_ref,'notes'] = 'offer outside of expctd bds: {}'.format(counter_offer)
                    self.debug_file.writeToDebug('offer outside of expctd bds: {}'.format(counter_offer))

                send_cancel_email = True
            else:
                #this is if there is more than one number in the message. I don't know what that would mean. It could
                #be something like "I can't do 140, but I could do 180.", in which case I'd probably want to take the
                #larger number. I'll change this later maybe.
                self.df.loc[self.df['email_id']==orig_ref,'notes'] = 'mltple nums found: {}'.format(', '.join(list(map(str,num_found))))
                self.debug_file.writeToDebug('mltple nums found: {}'.format(', '.join(list(map(str,num_found)))))
        else:
            self.debug_file.writeToDebug('no nums found in main message.')
            not_avail_list = ['sold','available','bought']
            if any([(entry in main_msg) for entry in not_avail_list]):
                self.debug_file.writeToDebug('Some word indicating that is unavailable found, marking as unavailable.')
                self.df.loc[self.df['email_id']==orig_ref,'available'] = 0


        return(send_cancel_email)


















#
