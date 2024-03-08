from sv_utils import *
from sv_models import *
from config import *
from api import *

def download_thread(
	app: fs.Flask,
	boltz: Boltz,
	id: str,
	tracks: list[BoltzTrack],
	path: str
):
	with app.app_context():
		pm = fs.current_app.config[PROGRESS_MANAGER]

		# Check if already exists in db
		pl = DBTrackEntry.query.filter_by(id = id).first()
		if pl:
			progress: DownloadProgrss = pm.get(id)
			progress.status = DownloadStatus.DONE
			return

		for track in tracks:
			track_progress = pm.get(id).tracks[track.id]
			track_progress["status"] = DownloadStatus.DOWNLOADING

			mp3 = boltz.download_track(track, path)
			if not mp3.is_valid:
				track_progress["status"] = DownloadStatus.FAILED
				continue

			track_progress["status"] = DownloadStatus.CONVERTING
			if not boltz.set_tags(mp3, len(tracks)):
				track_progress["status"] = DownloadStatus.FAILED
				continue

			track_progress["status"] = DownloadStatus.DONE

			tracks = pm.get(id).tracks
			tracks[track.id] = track_progress

		pm.get(id).status = DownloadStatus.DONE

		# Generating zip and deleting the directory
		shutil.make_archive(path, "zip", path)
		size = os.path.getsize(path + ".zip")
		shutil.rmtree(path)

		# NOTE: This way doesnt check whether the currently downloaded file is less than max download size
		# Deleting old tracks when memory is full
		db_tracks = DBTrackEntry.query.all()
		db_size = 0
		for track in db_tracks:
			db_size += track.size

		while db_size > MAX_DOWNLOAD_SIZE:
			least_dl_track = DBTrackEntry.query.order_by(DBTrackEntry.downloads).first()
			print(f"db_size: {db_size}, Deleting: {least_dl_track}")
			os.remove(DOWNLOAD_ROOT + least_dl_track.id + ".zip")
			pdb.session.delete(least_dl_track)
			pdb.session.commit()

			db_tracks = DBTrackEntry.query.all()
			db_size = 0
			for track in db_tracks:
				db_size += track.size

		# Appending in database
		new_track = DBTrackEntry(
			id = id,
			downloads = 0,
			size = size
		)
		pdb.session.add(new_track)
		pdb.session.commit()


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
	pm = fs.current_app.config[PROGRESS_MANAGER]
	if not pm.exists(url.id):
		progress = DownloadProgress(url.id)
		for track in tracks:
			progress.append_track(track)

		pm.append(progress)

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
	#if pl_id not in pm:
	# if not pm.exists(pl_id):

	# progress = pm[pl_id]
	progress = fs.current_app.config[PROGRESS_MANAGER].get(pl_id)
	if not progress:
		return Result(
			log = f"Cannot find download progress for pl_id: {pl_id}",
			status = 500
		)

	return Result(
		data = progress.to_dict(),
		log = f"Progress for pl_id: {pl_id}"
	)

def get_file(pl_id: str) -> fs.Response:
	pl = DBTrackEntry.query.filter_by(id = pl_id).first()
	if not pl:
		return result_to_response(Result(
			log = f"Cannot find playlist of id: {pl_id} in database",
			status = 500
		))

	pl.downloads += 1
	pdb.session.add(pl)
	pdb.session.commit()

	fs.current_app.config[PROGRESS_MANAGER].pop(pl_id)

	# if pl_id in pm:
	# 	pm.pop(pl_id)

	#NOTE: HARD CODED TO ONE DIRECTORY BACK (BE CAREFUL!!)
	return fs.send_file(".." + "/" + DOWNLOAD_ROOT + pl_id + ".zip")

