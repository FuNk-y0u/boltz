from sv_utils import *
from config import *
from api import *

def get_pl_id_from_user_pls(pls: dict) -> list[str]:
	pl_id = []
	items = pls["items"]
	for item in items:
		pl_id.append(item["id"])
	return pl_id

@boltz_route(fields = ["spotify_id"])
def fetch_user_data(payload: dict) -> Result:
	s_id = payload["spotify_id"]
	boltz = Boltz(CLIENT_ID, CLIENT_SECRET)

	#TODO: spotify_id is not checked if its valid or not
	data = boltz.sp.user_playlists(s_id)
	pl_ids = get_pl_id_from_user_pls(data)

	return Result(
		log = f"fetched playlist for user = {s_id}",
		status = 500,
		data = {
			"playlists": pl_ids
		}
	)

