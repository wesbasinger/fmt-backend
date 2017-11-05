import json

from db import insert


def add(event, context):

	data = json.loads(event['body'])

	result = insert(data)

	response = {
		"body" : json.dumps(result),
		"statusCode" : 200
	}

	return response
