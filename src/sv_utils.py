from inc import *
from sv_types import *


def verify_key(keys: list, json: dict) -> bool:
	return all(k in json for k in keys)


def result_to_response(result: Result) -> fs.Response:
	return fs.Response(
		json.dumps(result.__dict__),
		status = result.status,
		content_type = "application/json"
	)


def boltz_route(*args, **kwargs) -> any:
	# Grabbing the fields
	fields = []
	if "fields" in kwargs:
		fields = kwargs["fields"]

	def inner(func):
		@wraps(func)
		def decorated(*args, **kwargs) -> fs.Response:

			# Field guard
			payload = fs.request.get_json()
			if not verify_key(fields, payload):
				res = {
					"data": {},
					"log": "(" + "|".join(fields) + ") are the required fields.",
					"status": 500
				}
				return fs.Response(
					json.dumps(res),
					status = res["status"],
					content_type = "application/json"
				)

			# Running the wrapped function
			res: Result = func(payload, *args, **kwargs)
			return fs.Response(
				json.dumps(res.__dict__),
				status = res.status,
				content_type = "application/json"
			)

		return decorated
	return inner
