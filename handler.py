import json

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
