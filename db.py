import os

from utils import get_rounded_hours

from pymongo import MongoClient

from bson.objectid import ObjectId

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

		# encode object ID to be json safe
		doc['_id'] = str(doc['_id'])

		results.append(doc)

	return results

def get_active_sign_ins():

	results = []

	cursor = actives.find()

	for doc in cursor:

		# purge sign ins that were not signed out.
		if(get_rounded_hours(doc['geolocation']['timestamp']) > 12):

			actives.delete_one({"_id": doc['id']})

		else:

			flattened_and_encoded = {
				"_id" : str(doc['_id']),
				"name" : doc['name'],
				"castMemberName" : doc["castMemberName"],
				"castMemberId" : doc["castMemberId"],
				"session" : doc["session"],
				"comments" : doc["comments"],
				"timestamp" : doc["geolocation"]["timestamp"]
			}

			results.append(flattened_and_encoded)

	return results

def get_single_sign_in(str_id):

	doc = actives.find_one({'_id': ObjectId(str_id)})

	return doc

def add_hours(cast_id, rounded_hours):

	if rounded_hours == 0:

		return {"success" : True, "message" : "No accrued hours on the clock."}

	result = cast.update_one(
		{"_id" : ObjectId(cast_id)},
		{
			"$inc" : {
				"hours.SP18" : rounded_hours
			}
		}
	)

	if result.modified_count == 1:

		return {"success" : True}

	else:

		return {"success" : False, "message": "Update operation failed."}

def delete_active(str_id):

	result = actives.delete_one({"_id" : ObjectId(str_id)})

	if result.deleted_count == 1:

		return {"success" : True}

	else:

		return {"success" : False, "message" : "Delete operation failed."}

def add_history(cast_id, history_dict):

	result = cast.update_one(
		{"_id" : ObjectId(cast_id)},
		{
			"$push" : {
				"history" : history_dict
			}
		}
	)

	if result.modified_count == 1:

		return {"success" : True}

	else:

		return {"success" : False, "message": "Update operation failed."}
