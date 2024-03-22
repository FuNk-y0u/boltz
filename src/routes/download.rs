use crate::api::boltz::Boltz;
use crate::api::boltz_error::Error;

use std::result::Result;
use std::sync::Mutex;
use std::collections::HashMap;
use reqwest::Client;
use actix_web::{ post, web, HttpResponse };
use serde::{ Serialize, Deserialize };

#[derive(Debug, Serialize, Deserialize)]
pub struct DownloadPayload {
	playlist_id: String
}

#[post("/download")]
pub async fn download(
	data: web::Data<Mutex<Boltz>>,
	payload: web::Json<DownloadPayload>
) -> Result<HttpResponse, Error> {
	let mut boltz = data.lock().unwrap();
	let playlist = boltz
		.fetch_playlist(&payload.playlist_id).await?;

	for item in playlist.tracks.items {
		let file_name = boltz.download_track(&item.track).await?;
		boltz.set_mp3_tags_to_track(&file_name, &item.track).await?;
	}

	let mut res = HashMap::new();
	res.insert("playlist_id", &payload.playlist_id);

	Ok(HttpResponse::Ok().json(res))
}

