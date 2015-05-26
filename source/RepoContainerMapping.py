from .database_src import database

class RepoContainerMapping:
	def __init__(self):
		self.dbConn = database.DataBase()
		self.COLLECTION_NAME = "RepoContainerMapping"
				
	def printAllRecords(self):
		self.dbConn.getAllRecord(self.COLLECTION_NAME)
		
	def saveMapping(self,mapping):
		return self.dbConn.addRecord(self.COLLECTION_NAME,mapping)
		
	def getMapping(self,mappingKey):
		return self.dbConn.getRecord(self.COLLECTION_NAME,mappingKey)
	
	def checkMapping(self,mapping):
		oldMapping = self.getMapping({'dockerImageRepo':mapping['dockerImageRepo']})
		print(oldMapping)
		if not oldMapping:
			print(self.saveMapping(mapping))
			
		
	