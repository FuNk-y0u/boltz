from sv_inc import *
from sv_utils import *
from config import *
from sv_types import *
from boltz_api import *


@boltz_route(fields = ["keyword", "search_type"])
def search(payload: dict) -> Result:
	boltz = Boltz(CLIENT_ID, CLIENT_SECRET)
	results = boltz.search_song(payload["keyword"], payload["search_type"])

	if not results:
		return Result(
			log = f"Cannot find result with keyword: {payload['keyword']}",
			status = 404
		)

	value = {}
	for i, result in enumerate(results):
		value.update({i: result.to_json()})

	return Result(data = value)

