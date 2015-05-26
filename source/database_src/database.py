class DataBase:
        def __init__(self):
            from pymongo import MongoClient
            client = MongoClient()
            self.db = client.test

        def addRecord(self,collectionName,record):
            return self.db[collectionName].insert_one(record)

        def getRecord(self,collectionName,record):
            return self.db[collectionName].find_one(record)

#        def getAllRecord(self):
#            for record in self.db[collectionName].find():
#                print(record)

        def getAllRecord(self):
            for record in self.db.coll.find():
                print(record)

        def updateRecord(self,collectionName,updateKey,newRecord):
            oldRecord = self.getRecord(collectionName,updateKey)
            print(oldRecord)
            for key in newRecord:
                 oldRecord[key] = newRecord[key]
            print(oldRecord)
            self.db.coll.update({'_id':oldRecord['_id']},oldRecord)
