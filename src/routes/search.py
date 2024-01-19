from sv_inc import *
from sv_utils import *
from config import *
from boltz_types import *

from api.boltz import *

@boltz_route
def search() -> Result:
	payload = fs.request.get_json()

	if not verify_key(["keyword"], payload):
		return Result(
			error = Error("'keyword' field is not provided.", status = 500)
		)

	boltz = Boltz(CLIENT_ID, CLIENT_SECRET)
	results = boltz.search_song(payload["keyword"], BoltzSearchTypes.playlist)

	if not results:
		return Result(
			error = Error(f"Cannot find result with keyword: {payload['keyword']}", status = 404)
		)

	results = [json.dumps(result.to_json()) for result in results]
	return Result(results)

