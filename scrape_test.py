from bs4 import BeautifulSoup
import requests

#phone and email
page_link = 'https://providence.craigslist.org/pts/d/ladder-rack-126-length-off-97/6651755000.html'
#just phone
#page_link = 'https://providence.craigslist.org/hsh/d/new-10-bag-of-grout/6664468227.html'
# fetch the content from url
page_response = requests.get(page_link, timeout=5)
# parse html
page_content = BeautifulSoup(page_response.content, 'html.parser')

reply_methods = page_content.find_all(class_='envelope')
print('reply methods:',reply_methods)

post_title = page_content.find_all(id='titletextonly')
print('title:',post_title)

price = page_content.find_all(class_='price')
print('price:',price)

post_info = page_content.find_all(class_='postinginfo')
#print('post info:')
#[print(piece) for piece in post_info]

post_id = [piece for piece in post_info if 'post id' in str(piece)]
print('post id:',post_id)

post_date = [piece for piece in post_info if 'posted' in str(piece)]
print('post date:',post_date)

post_update = [piece for piece in post_info if 'updated' in str(piece)]
print('post update:',post_update)


location = page_content.find_all(id='map')
print('GPS coords:',location)



exit(0)
try:
    page_response = requests.get(page_link, timeout=5)
    if page_response.status_code == 200:
        # extract
        pass
    else:
        print(page_response.status_code)
        # notify, try again
except requests.Timeout as e:
    print("It is time to timeout")
    print(str(e))




#
