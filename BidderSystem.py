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




    def processBatch(self,city):

        #Get posts for city
        print('getting posts for',city)
        city_posts = self.st.getCitySales('providence')[:3]
        print(city_posts)

        percents = [.6,.8,1.0]

        #For each post:
        for i,post in enumerate(city_posts):
            #scrape page, get info

            page_info = self.st.getPageInfo(post)
            page_info.printAll()

            percent_offered = percents[i%len(percents)]
            price_offered = self.st.getRoundPrice(page_info.price,percent_offered)

            print('\n\noffering {} percent, which is rounded to ${}\n'.format(100*percent_offered,price_offered))

            if abs(percent_offered - 1.0)<.01:
                msg_type = 'available'
            else:
                msg_type = 'polite'

            email_id = self.et.sendEmailOffer(page_info, price_offered,msg_type)

            self.db.addToDatabase(page_info,email_id,percent_offered,price_offered,msg_type)




            #check if phone number (maybe other stuff?) is in database
            #if not:
                #format email
                #send email
                #enter info in database
