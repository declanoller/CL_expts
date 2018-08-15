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
        'counter_offer'
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
        'counter_offer' : [np.nan]
        })

        self.df = self.df.append(add_df,ignore_index=True)
        self.debug_file.writeToDebug('adding to df and writing to file')
        #print('adding to df and writing to file')
        #print(self.df.head())
        self.writeCSV()


    def updateWithReply(self,reply_email):

        send_cancel_email = False
        self.readCSV()
        print('\n***********************************************\n')

        if reply_email['References'] is not None:
            ref_list = reply_email['References'].split()
            orig_ref = [id for id in ref_list if 'TITTYWHISKERS88' in id]
            if orig_ref!=[]:
                orig_ref = orig_ref[0]
                #Check if this email is actually responding to one in the DB, and that it hasn't been responded to yet
                if (orig_ref in self.df['email_id'].values) and (self.df.loc[self.df['email_id']==orig_ref,'reply_email_id'].values[0].isnull()):

                    #Get date in right format
                    dt_obj = datetime.strptime(reply_email['Date'],"%a, %d %b %Y %H:%M:%S %z").astimezone(self.east_tz)
                    dt_string = dt_obj.strftime("%Y-%m-%d_%H-%M-%S")

                    #Update the DB with the things we can
                    self.df.loc[self.df['email_id']==orig_ref,'date_rplied'] = dt_string
                    self.df.loc[self.df['email_id']==orig_ref,'replied'] = 1
                    self.df.loc[self.df['email_id']==orig_ref,'reply_email_id'] = reply_email['Message-ID']

                    #If it's multipart, you have to combine them.
                    if reply_email.is_multipart():
                        body = ''
                        for payload in reply_email.get_payload():
                            # if payload.is_multipart(): ...
                            body = body + payload.get_payload()
                    else:
                        body = reply_email.get_payload()

                    body_parts = body.split('\n>')
                    main_msg = body_parts[0]
                    main_msg = quopri.decodestring(main_msg).decode('utf-8')

                    print(main_msg)

                    num_found = re.findall(r'\d+', main_msg)
                    num_found = list(map(int,num_found))
                    print('\n\n')

                    #Did they accept or not?
                    if len(num_found)>0:
                        if len(num_found)==1:
                            #This will assume that if there's one number in there, it's probably their counter offer.
                            counter_offer = num_found[0]

                            orig_price = self.df.loc[self.df['email_id']==orig_ref,'price'].values[0]
                            orig_offer = self.df.loc[self.df['email_id']==orig_ref,'price_offd'].values[0]

                            if counter_offer<=orig_price and counter_offer>=orig_offer:
                                self.df.loc[self.df['email_id']==orig_ref,'counter_offer'] = counter_offer
                                self.df.loc[self.df['email_id']==orig_ref,'available'] = 1

                            send_cancel_email = True
                    else:
                        not_avail_list = ['sold','available','bought']
                        if any([(entry in main_msg) for entry in not_avail_list]):
                            self.df.loc[self.df['email_id']==orig_ref,'available'] = 0

                    self.writeCSV()







    def readCSV(self):
        self.df = pd.read_csv(self.csv_fname,delimiter='\t')


    def writeCSV(self):
        self.df.to_csv(self.csv_fname,sep="\t",index=False)


    def getDateTimeStr(self):
        dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return(dt_string)


    def getPostFromID(self,ID):
        p = Post(self.df.loc[self.df['email_id']==ID,'link'].values[0])

        p.email = self.df.loc[self.df['email_id']==ID,'email'].values[0]
        p.title = self.df.loc[self.df['email_id']==ID,'title'].values[0]

        p.stuff = stuff






#
