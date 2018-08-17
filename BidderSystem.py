from EmailTools import EmailTools
from ScrapingTools import ScrapingTools
from DatabaseTools import DatabaseTools
from DebugFile import DebugFile



class BidderSystem:

    def __init__(self,notes=''):
        self.df = DebugFile(notes)
        self.db = DatabaseTools(self.df)
        self.et = EmailTools(self.df)
        self.st = ScrapingTools(self.df)
        self.notes = notes




    def processBatch(self,location,send_emails=True):

        #Get posts for location
        print('\n\ngetting posts for',location)
        location_posts = self.st.getLocationPosts(location)[:6]
        print('doing this many posts:', len(location_posts))

        self.df.writeToDebug('getting posts for ' + location + ':\n' + '\n'.join(location_posts))

        percents = [.3,.5,.6,.7,.8,.9,1.0]
        self.df.writeToDebug('percents used: {}'.format(percents))

        #For each post:
        for i,post in enumerate(location_posts):
            #scrape page, get info

            page_info = self.st.getPageInfo(post)
            print()
            print(page_info.title)

            if page_info.email is not None:

                if not self.db.isDuplicate(page_info):

                    self.df.writeToDebug('post items:')
                    self.df.writeToDebug('{}\n'.format(page_info.getPostItems()))
                    percent_offered = percents[i%len(percents)]
                    price_offered = self.st.getRoundPrice(page_info.price,percent_offered)

                    print('offering {} percent, which is rounded to ${}\n\n'.format(100*percent_offered,price_offered))

                    self.df.writeToDebug('offering {} percent, which is rounded to ${}\n'.format(100*percent_offered,price_offered))

                    if abs(percent_offered - 1.0)<.01:
                        msg_type = 'available'
                    else:
                        msg_type = 'polite'

                    self.df.writeToDebug('Message type: ' + msg_type)

                    if send_emails:
                        email_id = self.et.sendEmailOffer(page_info, price_offered,msg_type)

                    self.db.addToDatabase(page_info,email_id,percent_offered,price_offered,msg_type,location)

                else:
                    print('duplicate!')
                    self.df.writeToDebug('is duplicate, skipping.')
                    continue

            else:
                print('no valid email address, skipping')
                self.df.writeToDebug('no valid email address, skipping')
                continue



    def updateDB(self,send_cancel_emails = True):

        self.df.writeToDebug('Checking inbox and updating database.\n\n\n')

        self.df.writeToDebug('Getting unread emails...')
        new_mail = self.et.getUnreadEmails()
        self.df.writeToDebug('Done.')

        for mail in new_mail:
            print('\n\n')

            send_cancel = self.db.updateWithReply(mail)

            if send_cancel_emails and send_cancel:

                temp_post = self.db.getPostFromEmail(mail)
                self.et.sendCancelEmail(post)

        print('\n\n')




























#
