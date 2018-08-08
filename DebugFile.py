from datetime import datetime
import time


class DebugFile:


	def __init__(self,notes):
		#Prepare debug file

		self.debug_dir = 'debug_files'
		self.start_dt_string = self.getDateTimeStr()
		self.debug_fname = 'Debug_' + self.start_dt_string + '.txt'
		print('creating debug file:',self.debug_fname)

		self.full_path_name = self.debug_dir + '/' + self.debug_fname
		self.notes = notes

		fDebug = open(self.full_path_name,'w+')
		fDebug.write('Run notes: ' + self.notes + '\n\n\n')
		fDebug.close()



	def writeToDebug(self,write_string):
		fDebug = open(self.full_path_name,'a')
		dateString = datetime.now().strftime("[%H:%M:%S   %Y-%m-%d]")
		fDebug.write(dateString + '\t' + write_string + '\n')
		fDebug.close()

	def getDateTimeStr(self):
		dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		return(dt_string)





#
