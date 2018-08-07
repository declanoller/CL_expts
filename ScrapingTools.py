from selenium import webdriver
from time import sleep

class ScrapingTools:

    def __init__(self):
        self.br = webdriver.Firefox()


    def getPageInfo(self,page):
        self.br.get(page)
        load_wait = 2
        sleep(load_wait)

        reply_methods = self.br.find_element_by_class_name('envelope')
        print('\nreply methods:',reply_methods.text)

        post_title = self.br.find_element_by_id('titletextonly')
        print('\ntitle:',post_title.text)

        price = self.br.find_element_by_class_name('price')
        print('\nprice:',price.text)

        post_info = self.br.find_elements_by_class_name('postinginfo')
        print('\npost_info:')
        #[print(piece.text) for piece in post_info]


        #location = self.br.find_elements_by_id('map')
        '''location = self.br.find_elements_by_class_name('mapAndAttrs')
        print('GPS coords:')
        [print(piece.text) for piece in location]'''

        post_id = [piece.text for piece in post_info if 'post id' in piece.text][0]
        print('\npost id:',post_id)

        post_date = [piece.text for piece in post_info if 'posted' in piece.text][0]
        print('\npost date:',post_date)

        post_update = [piece.text for piece in post_info if 'updated' in piece.text][0]
        print('\npost update:',post_update)

        return(0)


    def getReplyEmail(self):
        #Right now this will assume that you're already on the page.

        link_elem = self.br.find_element_by_class_name('reply_button.js-only')
        #print(link_elem)

        link_elem.click()

        click_wait = 3
        sleep(click_wait)

        em = self.br.find_element_by_partial_link_text('sale.craigslist.org')

        print('reply email: ',em.text)

        return(0)


    def getCitySales(self,'city'):

        city_sales_link = 'https://{}.craigslist.org/d/for-sale/search/sss'.format(city)

        #max price: https://maine.craigslist.org/search/sss?max_price=1000


    def closeBrowser(self):
        self.br.quit()
