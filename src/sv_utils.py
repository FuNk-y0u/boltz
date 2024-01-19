from inc import *
from boltz_types import *


def verify_key(keys: list, json: dict) -> bool:
	return all(k in json for k in keys)


def boltz_route(func: any) -> any:
	@wraps(func)

	def decorated(*args, **kwargs) -> fs.Response:
		res: Result = func(*args, **kwargs)
		if res.has_value():
			#TODO: Hard coded for json only response
			return fs.Response(res.value, status = 200, content_type="application/json")
		return fs.Response(res.error.log, status = res.error.status)

	return decorated
