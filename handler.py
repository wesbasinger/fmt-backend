import os

import json

from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URI'])

db = client['fmt']

actives = db['actives']

def add(event, context):

	data = json.loads(event['body'])

	actives.insert_one(data)
