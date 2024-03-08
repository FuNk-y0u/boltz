
# ! File for all boltz models
from dataclasses import dataclass

@dataclass
class BoltzUrl:
	type:str
	id:str
	is_valid:bool

	def to_json(self) -> dict:
		return self.__dict__

@dataclass
class BoltzImage:
	width:int
	height:int
	url:str

	def to_json(self) -> dict:
		return self.__dict__

@dataclass
class BoltzArtist:
	name:str
	uri:str

@dataclass
class BoltzItem:
	album_images:list[BoltzImage]
	album_name:str
	release_date:str
	total_tracks:int
	artists: list[BoltzArtist]
	id:str
	name:str
	track_number:int

@dataclass
class BoltzAlbum:
	name:str
	year:str
	total_tracks:int
	cover:str
	artists:list[BoltzArtist]

@dataclass
class BoltzTrack:
	id:str
	name:str
	position:int
	album:BoltzAlbum
	artist:str
	genre:str

@dataclass
class BoltzMP3:
	is_valid:bool
	track:BoltzTrack
	mp3_filename:str
	index:int


@dataclass
class BoltzSearchTypes:
	track:str = "track"
	album:str = "album"
	playlist:str = "playlist"

@dataclass
class BoltzSearchResult:
	url: BoltzUrl
	title: str
	artist: str
	image: BoltzImage

	def to_json(self) -> dict:
		d = self.__dict__
		d["url"] = self.url.to_json()
		d["image"] = self.image.to_json()
		return d

