from EmailTools import EmailTools
from ScrapingTools import ScrapingTools
from DatabaseTools import DatabaseTools
from DebugFile import DebugFile
from BidderSystem import BidderSystem



location = 'denver'

bs = BidderSystem(location + '_test')

bs.processBatch(location,send_emails=False)


exit(0)




#
