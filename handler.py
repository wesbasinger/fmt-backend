import json

import db

SESSION = "SP18"

def add(event, context):

	data = json.loads(event['body'])

	result = db.insert(data)

	response = {
		"body" : json.dumps(result),
		"statusCode" : 200
	}

	return response

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
