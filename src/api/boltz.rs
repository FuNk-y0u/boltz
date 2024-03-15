use std::result::Result;
use reqwest::Client;
use youtube_dl::{ YoutubeDl, SearchOptions };
use id3::{ Tag, TagLike, Timestamp, Version, frame::{ Picture, PictureType } };
use std::time::SystemTime;
use std::str::FromStr;

use super::boltz_model::{ AccessToken, Playlist, Track };
use super::boltz_error::Error;

// TODO: Maybe take api url as a param to the boltz constructor
const API_URL: &str = "https://api.spotify.com/v1";

pub struct Boltz {
	pub rq_client: Client,
	pub token: AccessToken,
	pub download_path: String,
}

impl Boltz {
	pub async fn new(client_id: &str, client_secret: &str, download_path: String) -> Result<Boltz, Error> {
		let rq_client = Client::new();
		let token = Self::fetch_token(&rq_client, client_id, client_secret).await?;
		Ok(Boltz {
			rq_client: rq_client,
			token: token,
			download_path: download_path
		})
	}

	async fn fetch_token(
		rq_client: &Client, client_id: &str, client_secret: &str
	) -> Result<AccessToken, Error> {
		let url = "https://accounts.spotify.com/api/token";
		let body = format!(
			"grant_type=client_credentials&client_id={}&client_secret={}",
			client_id, client_secret
		);

		let mut token = rq_client
			.post(url)
			.header("Content-Type", "application/x-www-form-urlencoded")
			.body(body)
			.send()
			.await?
			.json::<AccessToken>()
			.await?;

		let now = SystemTime::now()
			.duration_since(SystemTime::UNIX_EPOCH)
			.unwrap()
			.as_secs();

		token.expires_at = Some(now + token.expires_in);

		Ok(token)
	}

	pub async fn fetch_playlist(&self, playlist_id: &str) -> Result<Playlist, Error> {
		let playlist = self.rq_client
			.get(format!("{API_URL}/playlists/{playlist_id}"))
			.header("Authorization", format!(
				"{} {}", self.token.token_type, self.token.access_token
			))
			.send()
			.await?
			.json::<Playlist>()
			.await?;

		Ok(playlist)
	}

	pub async fn download_track(&self, track: &Track) -> Result<String, Error> {
		let query = format!(
			"{} - {} (Lyrics)",
			track
				.artists
				.iter()
				.map(|x| x.name.clone())
				.collect::<Vec<_>>()
				.join(" "),
			track.name
		);

		let search = SearchOptions::youtube(&query);
		let _ = YoutubeDl::search_for(&search)
			.extract_audio(true)
			.extra_arg("--audio-format")
			.extra_arg("mp3")
			.output_template(&query)
			.download_to(&self.download_path)?;

		let file_name = format!("{query}.mp3");
		Ok(file_name)
	}

	pub async fn set_mp3_tags_to_track(&self, file_name: &str, track: &Track) -> Result<(), Error> {
		let path = format!("{}/{file_name}", self.download_path);
		let mut tag = Tag::read_from_path(&path)?;
		tag.set_album(&track.album.name);
		tag.set_date_released(
			Timestamp::from_str(&track.album.release_date)
			.map_err(|_| Error::TimeParse("Failed to convert string to timestamp.".to_string()))?
		);

		if track.album.images.len() > 0 {
			let img_bytes = self.rq_client
				.get(&track.album.images[0].url)
				.send()
				.await?
				.bytes()
				.await?
				.into_iter()
				.collect::<Vec<_>>();

			tag.add_picture(Picture {
				mime_type: "image/jpeg".to_string(),
				picture_type: PictureType::Other,
				description: "Album Cover".to_string(),
				data: img_bytes,
			});
		}
		tag.write_to_path(&path, Version::Id3v24)?;
		Ok(())
	}
}
