use reqwest::{ Client, Result };
use serde::{ Serialize, Deserialize };
use std::option::Option;
use std::time::SystemTime;

#[derive(Debug, Serialize, Deserialize)]
pub struct AccessToken {
	pub access_token: String,
	pub token_type: String,
	pub expires_in: u64,
	pub expires_at: Option<u64>
}

pub struct Boltz {
	pub rq_client: Client,
	pub token: AccessToken
}

impl Boltz {
	pub async fn new(client_id: &str, client_secret: &str) -> Result<Boltz> {
		let rq_client = Client::new();
		let token = Self::fetch_token(&rq_client, client_id, client_secret).await?;
		Ok(Boltz {
			rq_client: rq_client,
			token: token
		})
	}

	async fn fetch_token(
		rq_client: &Client, client_id: &str, client_secret: &str
	) -> Result<AccessToken> {
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
}
