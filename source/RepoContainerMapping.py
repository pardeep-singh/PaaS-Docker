from .database_src import database

class RepoContainerMapping:
	def __init__(self):
		self.dbConn = database.DataBase()
		self.COLLECTION_NAME = "RepoContainerMapping"
		self.MAPPING_KEY = 'dockerImageRepo'
				
	def printAllRecords(self):
		self.dbConn.getAllRecord(self.COLLECTION_NAME)
		
	def saveMapping(self,mapping):
		return self.dbConn.addRecord(self.COLLECTION_NAME,mapping)
		
	def getMapping(self,mappingKey):
		return self.dbConn.getRecord(self.COLLECTION_NAME,mappingKey)
	
	def updateMapping(self,updateKey,newFields):
		self.dbConn.updateRecord(self.COLLECTION_NAME,updateKey,newFields)

	def getPortsNContainerID(self,mapping):
		oldMapping = self.getMapping({self.MAPPING_KEY:mapping[self.MAPPING_KEY]})
		print(oldMapping)
		if oldMapping:
			return (oldMapping['portsMapping'],oldMapping['containerID'])
		else:
			return ({},'')
	
	def addPortsNContainerID(self,dockerImageRepo,portsUsed,containerID):
		updateKey = {self.MAPPING_KEY:dockerImageRepo}
		newFields = {'portsMapping':portsUsed,'containerID':containerID}
		self.updateMapping(updateKey,newFields)
		
			
			
		
	