import pandas as pd
from datetime import datetime
import subprocess
from os import path
import numpy as np


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
        'offer_accptd',
        'replied',
        'date_cntctd',
        'date_rplied',
        'location',
        'msg_type',
        'available'
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





    def addToDatabase(self,post,email_id,percent_offered,price_offered,msg_type,location):

        self.readCSV()

        add_df = pd.DataFrame({
        'link' : [post.page],
        'post_ID' : [post.id],
        'email' : [post.email],
        'email_id' : [email_id],
        'title' : [post.title],
        'price' : [post.price],
        'item_type' : [np.nan],
        'prcnt_offd' : [percent_offered],
        'price_offd' : [price_offered],
        'offer_accptd' : [0],
        'replied' : [0],
        'date_cntctd' : [self.getDateTimeStr()],
        'date_rplied' : [np.nan],
        'location' : [location],
        'msg_type' : [msg_type],
        'available' : [np.nan]
        })

        self.df = self.df.append(add_df,ignore_index=True)
        self.debug_file.writeToDebug('adding to df and writing to file')
        #print('adding to df and writing to file')
        #print(self.df.head())
        self.writeCSV()



    def readCSV(self):
        self.df = pd.read_csv(self.csv_fname,delimiter='\t')


    def writeCSV(self):
        self.df.to_csv(self.csv_fname,sep="\t",index=False)


    def getDateTimeStr(self):
        dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return(dt_string)













#
