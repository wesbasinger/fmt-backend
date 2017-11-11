import json
from time import time

import db
import utils

SESSION = "SP18"

def get_active_cast(event, context):

	results = db.get_active_cast(SESSION)

	print(results)

	response = {
		"body" : json.dumps(results),
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*"
        },
	}

	return response

def sign_in(event, context):

	data = json.loads(event['body'])

	# expects to get a json object as such...
	# {
	# 	"name" : string,
	# 	"castMember" : string,
	# 	"session" : string,
	# 	"comments": string,
	# 	"geolocation" : object
	# }

	# first run geolocation check on it
	try:

		geo_check_result = utils.check_geolocation(data['geolocation'])

	except KeyError:

		response = {
			"body" : json.dumps({"error": True, "message" : "Malformed data."}),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*"
	        },
		}

		return response



	if geo_check_result['error']:

		response = {
			"body" : json.dumps(geo_check_result),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*"
	        },
		}

		return response

	else:

		success_result = db.insert(data)

		response = {
			"body" : json.dumps(success_result),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*"
	        },
		}

		return response

def get_sign_ins(event, context):

	results = db.get_active_sign_ins()

	response = {
		"body" : json.dumps(results),
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*"
        },
	}

	return response

def process_sign_out(event, context):

	data = json.loads(event['body'])

	sign_in = db.get_single_sign_in(data['activeId'])

	# sample sign_in shown below

	# {
	# 	'_id': ObjectId('5a03b6c3b915df000104d56e'),
	# 	'name': 'Wesl', 'castMemberName':
	# 	'Amy Basinger', 'castMemberId':
	# 	'undefined', 'session': 'SP18 - Beauty and the Beast',
	# 	'comments': 'sdf',
	# 	'geolocation': {
	# 		'latitude': 32.6034122,
	# 		'longitude': -96.86327759999999,
	# 		'timestamp': 1510192829544
	# 	}
	# }

	now = time()

	elapsed_seconds = now - float(sign_in['geolocation']['timestamp'])/1000

	print("Elapsed seconds: ", elapsed_seconds)

	response = {
		"body" : json.dumps({"success" : True}),
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*"
        },
	}

	return response
