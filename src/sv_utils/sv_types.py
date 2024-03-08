from .sv_inc import *
from api import *

class Result:
	def __init__(
			self,
			data: dict = {},
			log: str = "",
			status: int = 200
		):
		self.data = data
		self.log = log
		self.status = status

class DownloadStatus:
	WAITING = "WAITING"
	DOWNLOADING = "DOWNLOADING"
	CONVERTING = "CONVERTING"
	DONE = "DONE"
	FAILED = "FAILED"

class DownloadProgress:
	def __init__(self, pl_id: str):
		self.pl_id: str = pl_id
		self.status: DownloadStatus = DownloadStatus.DOWNLOADING
		self.tracks: dict[str, dict[str, str]] = {}

	def append_track(self, track: BoltzTrack):
		self.tracks.update({
			track.id: {
				"name": track.name,
				"status": DownloadStatus.WAITING
			}
		})

	def to_dict(self) -> dict:
		return self.__dict__

class ProgressManager:
	def __init__(self):
		self.progress: dict[str, DownloadProgress] = {}

	def exists(self, id: str) -> bool:
		return id in self.progress

	def append(self, progress: DownloadProgress):
		self.progress.update({
			progress.pl_id: progress
		})

	def get(self, id: str) -> DownloadProgress | None:
		if id in self.progress:
			return self.progress[id]
		return None

	def pop(self, id: str) -> DownloadProgress | None:
		if id in self.progress:
			return self.progress.pop(id)
		return None

	def to_dict(self) -> dict:
		res = {}
		for id in self.progress:
			res.update({
				id: self.progress[id].to_dict()
			})
		return res

