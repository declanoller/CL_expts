from EmailTools import EmailTools
from ScrapingTools import ScrapingTools
from DatabaseTools import DatabaseTools
from DebugFile import DebugFile
from BidderSystem import BidderSystem


bs = BidderSystem()

bs.updateDB()


exit(0)


df = DebugFile('testingtesting')


et = EmailTools(df)

et.getUnreadEmails()






#
