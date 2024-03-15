use crate::api::boltz::Boltz;
use reqwest::{ Client, Result };
use actix_web::{ post, web, HttpResponse };
use serde::{ Serializable, Deserialziable };

#[derive(Serializable, Deserialziable)]
pub struct DownloadPayload {
}

#[post("/download")]
async fn download() -> HttpResponse {
}

