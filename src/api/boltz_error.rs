use std::fmt;
use reqwest;
use youtube_dl;
use id3;
use actix_web::{ HttpResponse, body::BoxBody, http::StatusCode, error::ResponseError };
use serde::{ Serialize, Deserialize };

#[derive(Debug, Serialize, Deserialize)]
pub struct SpotifyErrorInner {
	pub status: u16,
	pub message: String
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SpotifyError {
	pub error: SpotifyErrorInner
}

#[derive(Debug)]
pub enum Error {
	IO(std::io::Error),
	Reqwest(reqwest::Error),
	Ytdl(youtube_dl::Error),
	ID3(id3::Error),
	TimeParse(String),
	Web(StatusCode, String)
}

impl fmt::Display for Error {
	fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
		match self {
			Error::IO(io_err)       => write!(f, "{}", io_err),
			Error::Reqwest(rq_err)  => write!(f, "{}", rq_err),
			Error::Ytdl(yt_err)     => write!(f, "{}", yt_err),
			Error::ID3(id3_err)     => write!(f, "{}", id3_err),
			Error::TimeParse(t_err) => write!(f, "{}", t_err),
			Error::Web(code, body)  => write!(f, "Status: {}, Body: {}", code, body)
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

impl ResponseError for Error {
	fn status_code(&self) -> StatusCode {
		match self {
			&Error::IO(_)        => StatusCode::INTERNAL_SERVER_ERROR,
			&Error::Reqwest(_)   => StatusCode::INTERNAL_SERVER_ERROR,
			&Error::Ytdl(_)      => StatusCode::INTERNAL_SERVER_ERROR,
			&Error::ID3(_)       => StatusCode::INTERNAL_SERVER_ERROR,
			&Error::TimeParse(_) => StatusCode::INTERNAL_SERVER_ERROR,
			&Error::Web(code, _) => code
		}
	}


// TODO: Revisit this code, Its a dumpster fire of reference and cloning

	fn error_response(&self) -> HttpResponse<BoxBody> {
		match self {
			Error::IO(err) => {
				HttpResponse::build(StatusCode::INTERNAL_SERVER_ERROR)
					.body(err.to_string())
			},
			Error::Reqwest(err) => {
				HttpResponse::build(StatusCode::INTERNAL_SERVER_ERROR)
					.body(err.to_string())
			},
			Error::Ytdl(err) => {
				HttpResponse::build(StatusCode::INTERNAL_SERVER_ERROR)
					.body(err.to_string())
			},
			Error::ID3(err) => {
				HttpResponse::build(StatusCode::INTERNAL_SERVER_ERROR)
					.body(err.to_string())
			},
			Error::TimeParse(err) => {
				HttpResponse::build(StatusCode::INTERNAL_SERVER_ERROR)
					.body((*err).clone())
			},
			Error::Web(code, body) => {
				HttpResponse::build(*code).body((*body).clone())
			}
		}
	}
}

