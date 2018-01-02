import json
from time import time

import db
import utils

SESSION = "SP18"

def add_cast(event, context):

	data = json.loads(event['body'])

	result = db.add_cast(data)

	response = {
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*",
		   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
        },
	}

	if result:

		response['body'] = json.dumps(result)

	else:

		response['body'] = json.dumps({"error" :True, "message" : "Could not insert cast."})

	return response


def get_active_cast(event, context):

	results = db.get_active_cast(SESSION)

	response = {
		"body" : json.dumps(results),
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*",
		   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
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

		geo_check_result = utils.check_geolocation(data['geolocation'], work_from_home=data['workFromHome'])

	except:

		response = {
			"body" : json.dumps({"error": True, "message" : "Error while processing timestamp and geolocation.  Try refreshing the page."}),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*",
			   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
	        },
		}

		return response



	if geo_check_result['error']:

		response = {
			"body" : json.dumps(geo_check_result),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*",
			   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
	        },
		}

		return response

	else:

		history_dict = {

			"name" : data['name'],
			"session" : data['session'],
			"comments" : data['comments'],
			"datestamp" : utils.make_datestamp(data['geolocation']['timestamp'], is_JS=True),
			"cast_member" : data['castMemberName'],
			"type" : "sign_in",
			"remote" : data['workFromHome'],
			"elapsed_hours" : "N/A"
		}

		db.add_history(data['castMemberId'], history_dict)

		success_result = db.insert(data)

		response = {
			"body" : json.dumps(success_result),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*",
			   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
	        },
		}

		return response

def get_sign_ins(event, context):

	results = db.get_active_sign_ins()

	response = {
		"body" : json.dumps(results),
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*",
		   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
        },
	}

	return response

def process_sign_out(event, context):

	data = json.loads(event['body'])

	# first run geolocation check on it
	try:

		geo_check_result = utils.check_geolocation(data['geolocation'], work_from_home=data['workFromHome'])

	except:

		response = {
			"body" : json.dumps({"error": True, "message" : "Error while processing timestamp and geolocation.  Try refreshing the page."}),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*",
			   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
	        },
		}

		return response


	if geo_check_result['error']:

		response = {
			"body" : json.dumps(geo_check_result),
			"statusCode" : 200,
			"headers" : {
	           "Access-Control-Allow-Origin" : "*",
			   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
	        },
		}

		return response


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

	# get_rounded_hours takes a javascript timestamp
	rounded_hours = utils.get_rounded_hours(sign_in['geolocation']['timestamp'])

	result = db.add_hours(sign_in['castMemberId'], rounded_hours)

	response = {
		"statusCode" : 200,
		"headers" : {
           "Access-Control-Allow-Origin" : "*",
		   "Access-Control-Allow-Methods" : "GET, POST, DELETE"
        },
	}

	if result['success']:

		result = db.delete_active(data['activeId'])

		history_dict = {

			"name" : sign_in['name'],
			"session" : sign_in['session'],
			"comments" : sign_in['comments'],
			"datestamp" : utils.make_datestamp(time(), is_JS=False),
			"cast_member" : sign_in['castMemberName'],
			"type" : "sign_out",
			"remote" : data['workFromHome'],
			"elapsed_hours" : rounded_hours
		}

		db.add_history(sign_in['castMemberId'], history_dict)

		if result['success']:

			response['body'] = json.dumps({"success" : True, "message" : "Hours added."})

		else:

			response['body'] = json.dumps({"success" : False, "message" : "Deletion failed."})

	else:

		response['body'] = json.dumps({"success" : False, "message" : result['message']})



	return response
