use std::fmt;
use reqwest;
use youtube_dl;
use id3;

#[derive(Debug)]
pub enum Error {
	IO(std::io::Error),
	Reqwest(reqwest::Error),
	Ytdl(youtube_dl::Error),
	ID3(id3::Error),
	TimeParse(String)
}

impl fmt::Display for Error {
	fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
		match self {
			Error::IO(io_err)       => write!(f, "{}", io_err),
			Error::Reqwest(rq_err)  => write!(f, "{}", rq_err),
			Error::Ytdl(yt_err)     => write!(f, "{}", yt_err),
			Error::ID3(id3_err)     => write!(f, "{}", id3_err),
			Error::TimeParse(t_err) => write!(f, "{}", t_err)
		}
	}
}

impl std::error::Error for Error {}

impl From<std::io::Error> for Error {
	fn from(err: std::io::Error) -> Self {
		Error::IO(err)
	}
}

impl From<reqwest::Error> for Error {
	fn from(err: reqwest::Error) -> Self {
		Error::Reqwest(err)
	}
}

impl From<youtube_dl::Error> for Error {
	fn from(err: youtube_dl::Error) -> Self {
		Error::Ytdl(err)
	}
}

impl From<id3::Error> for Error {
	fn from(err: id3::Error) -> Self {
		Error::ID3(err)
	}
}

