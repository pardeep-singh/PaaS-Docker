from .database_src import database

class WordpressMapping:
	def __init__(self):
		self.dbConn = database.DataBase()
		self.COLLECTION_NAME = "WordpressMapping"
		self.MAPPING_KEY = 'dockerImageRepo'
				
	def printAllRecords(self):
		self.dbConn.getAllRecord(self.COLLECTION_NAME)
		
	def saveMapping(self,mapping):
		return self.dbConn.addRecord(self.COLLECTION_NAME,mapping)
		
	def getMapping(self,mappingKey):
		return self.dbConn.getRecord(self.COLLECTION_NAME,mappingKey)
	
	def updateMapping(self,updatedRecrd):
		self.dbConn.updateRecordValues(self.COLLECTION_NAME,updatedRecrd)

	def getExistingMapping(self,ownerName,repoName,branchName):
		mapping = self.getMapping({'ownerName':ownerName,'repoName':repoName,"branchName":branchName})
		return mapping

	def saveNewMapping(self,mapping):
		self.saveMapping(mapping)

	def updatePortNContainerID(self,mapping):
		self.updateMapping(mapping)	