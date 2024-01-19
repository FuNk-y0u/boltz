from sv_inc import *

@dataclass
class Error:
	log: str
	status: int

class Result:
	def __init__(self, value: any = None, error: Error = None):
		self.value = value
		self.error = error

	def has_value(self) -> bool:
		if self.error:
			return False
		return True

