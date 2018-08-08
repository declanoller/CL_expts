from EmailTools import EmailTools
from ScrapingTools import ScrapingTools
from DatabaseTools import DatabaseTools
from DebugFile import DebugFile
from BidderSystem import BidderSystem



location = 'lasvegas'

bs = BidderSystem(location + ' test')


bs.processBatch(location)








exit(0)

#post = bs.st.getPageInfo('https://providence.craigslist.org/rvs/d/1999-winnebago-adventurer-35/6665084568.html')
#print(post.reply_methods)





#
