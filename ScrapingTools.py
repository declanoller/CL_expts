from selenium import webdriver
from time import sleep

class ScrapingTools:

    def __init__(self,debug_file):
        self.debug_file = debug_file
        self.debug_file.writeToDebug('Starting FF webdriver')
        self.br = webdriver.Firefox()

    def getPageInfo(self,page):

        self.br.get(page)
        load_wait = 2
        sleep(load_wait)

        post = Post(page)

        post.reply_methods = self.br.find_element_by_class_name('envelope').text
        post.title = self.br.find_element_by_id('titletextonly').text
        post.price = int((self.br.find_element_by_class_name('price').text).replace('$',''))
        post_info = self.br.find_elements_by_class_name('postinginfo')

        post.id = [piece.text for piece in post_info if 'post id' in piece.text]
        if len(post.id)>0:
            post.id = post.id[0]
        else:
            post.id = None

        post.post_date = [piece.text for piece in post_info if 'posted' in piece.text]
        if len(post.post_date)>0:
            post.post_date = post.post_date[0]
        else:
            post.post_date = None

        post.post_update = [piece.text for piece in post_info if 'updated' in piece.text]
        if len(post.post_update)>0:
            post.post_update = post.post_update[0]
        else:
            post.post_update = None

        post.email = self.getReplyEmailAddress()

        '''print('\nreply methods:',post.reply_methods.text)
        print('\ntitle:',post.title.text)
        print('\nprice:',post.price.text)
        print('\npost_info:')
        print('\npost id:',post.id)
        print('\npost date:',post.post_date
        print('\npost update:',post.post_update)'''

        return(post)


    def getReplyEmailAddress(self):
        #Right now this will assume that you're already on the page.

        link_elem = self.br.find_element_by_class_name('reply_button.js-only')

        link_elem.click()

        click_wait = 3
        sleep(click_wait)

        em = self.br.find_element_by_partial_link_text('sale.craigslist.org')
        return(em.text)


    def getCitySales(self,city):

        max_price = 1000
        city_sales_link = 'https://{}.craigslist.org/d/for-sale/search/sss?max_price={}'.format(city,max_price)

        self.br.get(city_sales_link)
        load_wait = 3
        sleep(load_wait)

        sale_items = self.br.find_elements_by_class_name('result-title.hdrlnk')
        #print('\nsale_items:')
        #[print(piece.text,'\t',piece.get_attribute('href')) for piece in sale_items[:20]]
        #print('len:',len(sale_items))

        return([piece.get_attribute('href') for piece in sale_items])


    def __del__(self):
        print('closing browser via ST __del__')
        self.debug_file.writeToDebug('closing browser via ST __del__')
        self.br.quit()


    def getRoundPrice(self,price,percent):

        if abs(percent - 1.0)<.01:
            return(price)

        if price<1000:
            round_num = 20
        if price<100:
            round_num = 5
        if price<10:
            round_num = 1

        return(int(percent*price/round_num)*round_num)





class Post:

    def __init__(self,page):
        self.page = page
        self.reply_methods = None
        self.title = None
        self.price = None
        self.id = None
        self.post_date = None
        self.post_update = None
        self.email = None

    def printAll(self):
        print('\n\npost entries:')
        [print(entry) for entry in vars(self).items()]

    def getPostItems(self):
        return(vars(self).items())







#
