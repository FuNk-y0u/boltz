use serde::{ Serialize, Deserialize };
use std::option::Option;

#[derive(Debug, Serialize, Deserialize)]
pub struct AccessToken {
	pub access_token: String,
	pub token_type: String,
	pub expires_in: u64,
	pub expires_at: Option<u64>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Artist {
	pub name: String
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Image {
	pub url: String,
	pub width: i32,
	pub height: i32
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Album {
	pub name: String,
	pub release_date: String,
	pub images: Vec<Image>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Track {
	pub id: String,
	pub name: String,
	pub album: Album,
	pub artists: Vec<Artist>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
	pub track: Track
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Page<T> {
	pub items: Vec<T>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Playlist {
	pub name: String,
	pub id: String,
	pub tracks: Page<Item>
}

