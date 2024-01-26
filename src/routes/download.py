from sv_inc import *
from sv_utils import *
from config import *
from sv_types import *
from boltz_api import *

def download_thread(
	app: fs.Flask,
	boltz: Boltz,
	id: str,
	tracks: list[BoltzTrack],
	path: str
):
	with app.app_context():
		for i, track in enumerate(tracks):
			progress = fs.current_app.config[DOWNLOAD_PROGRESS][id]["tracks"][i]

			progress["status"] = DownloadStatus.DOWNLOADING
			mp3 = boltz.download_track(track, path)
			if not mp3.is_valid:
				progress["status"] = DownloadStatus.FAILED
				continue

			progress["status"] = DownloadStatus.CONVERTING
			if not boltz.set_tags(mp3, len(tracks)):
				progress["status"] = DownloadStatus.FAILED
				continue

			progress["status"] = DownloadStatus.DONE

			fs.current_app.config[DOWNLOAD_PROGRESS][id]["tracks"][i] = progress

		fs.current_app.config[DOWNLOAD_PROGRESS][id]["status"] = DownloadStatus.DONE
		shutil.make_archive(path, "zip", path)


@boltz_route(fields = ["url"])
def download(payload: dict) -> Result:
	boltz = Boltz(CLIENT_ID, CLIENT_SECRET)
	url = boltz.initialize_url(payload["url"])
	download_path = DOWNLOAD_ROOT + url.id

	if not url.is_valid:
		return Result(log = "Invalid spotify url", status = 500)

	tracks = boltz.fetch_tracks(url)
	if not tracks:
		return Result(
			log = f"Failed to fetch tracks: type = {url.type}, id = {url.id}",
			status = 500
		)

	# Appending download progress
	download_progress = {
		"status": DownloadStatus.DOWNLOADING,
		"tracks": []
	}
	for track in tracks:
		progress = DownloadProgress(track.id, track.name, DownloadStatus.WAITING)
		download_progress["tracks"].append(progress.__dict__)

	fs.current_app.config[DOWNLOAD_PROGRESS].update({
		url.id: download_progress
	})

	# Starting download
	threading.Thread(
		target = download_thread, args = (
			fs.current_app.config["APP"],
			boltz, url.id,
			tracks, download_path
		)
	).start()

	return Result(
		data = { "pl_id": url.id },
		log = f"Downloading url: {payload['url']}"
	)


@boltz_route(fields = ["pl_id"])
def get_status(payload: dict) -> Result:
	pl_id = payload["pl_id"]
	if pl_id not in fs.current_app.config[DOWNLOAD_PROGRESS]:
		return Result(
			log = f"Cannot find download progress for pl_id: {pl_id}",
			status = 500
		)

	progress = fs.current_app.config[DOWNLOAD_PROGRESS][pl_id]
	return Result(
		data = progress,
		log = f"Progress for pl_id: {pl_id}"
	)

def get_file(pl_id: str) -> fs.Response:
	#NOTE: Cannot refetch the same file again cuz pl_id is removed from progess pool
	if pl_id not in fs.current_app.config[DOWNLOAD_PROGRESS]:
		return result_to_response(Result(
			log = f"Cannot find download progress for pl_id: {pl_id}",
			status = 500
		))

	progress = fs.current_app.config[DOWNLOAD_PROGRESS][pl_id]
	if progress["status"] != DownloadStatus.DONE:
		return result_to_response(Result(
			log = f"Download is not completed for pl_id: {pl_id}",
			status = 500
		))

	fs.current_app.config[DOWNLOAD_PROGRESS].pop(pl_id)

	#NOTE: HARD CODED TO ONE DIRECTORY BACK (BE CAREFUL!!)
	return fs.send_file(".." + "/" + DOWNLOAD_ROOT + pl_id + ".zip")

