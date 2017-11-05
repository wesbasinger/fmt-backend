import os

from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URI'])

db = client['fmt']

actives = db['actives']

def insert(data):

	actives.insert_one(data)

	return {"success" : True}                                                                                                                                     
