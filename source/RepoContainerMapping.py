from .database_src import database

class RepoContainerMapping:
	def __init__(self):
		print("hello object created")
		
	def sayHello(self):
		print("hello world")
		
	def printAllRecords(self):
		db = database.DataBase()
		db.getAllRecord()
		
	