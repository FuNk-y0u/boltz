from sv_inc import *
from sv_utils import *
from config import *
from sv_types import *
from boltz_api import *


@boltz_route(fields = ["url"])
def download(payload: dict) -> Result:
	id = str(uuid.uuid4())
	download_path = DOWNLOAD_ROOT + id
	os.mkdir(download_path)

	boltz = Boltz(CLIENT_ID, CLIENT_SECRET, download_path)
	url = boltz.initialize_url(payload["url"])

	if not url.is_valid:
		return Result(log = "Invalid spotify url", status = 500)

	tracks = boltz.fetch_tracks(url)
	if not tracks:
		return Result(
			log = f"Failed to fetch tracks: type = {url.type}, id = {url.id}",
			status = 500
		)

	for track in tracks:
		mp3 = boltz.download_track(track)
		if not boltz.set_tags(mp3, len(tracks)):
			return Result(
				log = f"Failed to convert track to mp3: id = {track.id}, name = {track.name}",
				status = 500
			)

	shutil.make_archive(download_path, "zip", download_path)
	return Result(
		data = { "file_id": id },
		log = f"Sucessfully downloaded url: {payload['url']}"
	)

