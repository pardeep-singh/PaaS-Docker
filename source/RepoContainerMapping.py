from .database_src import database

class RepoContainerMapping:
	def __init__(self):
		self.dbConn = database.DataBase()
		self.COLLECTION_NAME = "RepoContainerMapping"
				
	def printAllRecords(self):
		dbConn.getAllRecord(self.collName)
		
	def saveMapping(self,mapping):
		return dbConn.addRecord(self.COLLECTION_NAME,mapping)
		
	