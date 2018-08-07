from EmailTools import EmailTools
from ScrapingTools import ScrapingTools






et = EmailTools()
st = ScrapingTools()

print('browser open?')

samplepage = 'https://providence.craigslist.org/pts/d/ladder-rack-126-length-off-97/6651755000.html'

st.getPageInfo(samplepage)

st.getReplyEmail()


st.closeBrowser()
