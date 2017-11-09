import os

from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URI'])

db = client['fmt']

actives = db['actives']

cast = db['cast']

def insert(data):

	actives.insert_one(data)

	return {"success" : True}

def get_active_cast(session):

	cursor = cast.find(
		{"activeSessions" : {"$in" : [session]}}
	)

	results = []

	for doc in cursor:

		results.append({"firstName":doc['firstName'], "lastName":doc['lastName'], "_id" : str(doc['_id'])})

	return results
