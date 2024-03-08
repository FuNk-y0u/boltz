from .sv_inc import *

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

@dataclass
class DownloadProgress:
	id: str
	name: str
	status: DownloadStatus

