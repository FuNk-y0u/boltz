mod boltz;

use std::process::exit;
use dotenv::dotenv;
use actix_web::{get, HttpServer, App, HttpResponse, middleware::Logger};

use boltz::boltz::Boltz;

#[get("/")]
async fn index() -> HttpResponse {
	HttpResponse::Ok()
		.body("Hello, World!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
	dotenv().ok();

	if std::env::var_os("RUST_LOG").is_none() {
		std::env::set_var("RUST_LOG", "info,void=error,void=debug");
	}

	env_logger::init();

	let server_ip = std::env::var("SERVER_IP")
		.expect("SERVER_IP environment variable needs to be set.");
	let server_port = std::env::var("SERVER_PORT")
		.expect("SERVER_PORT environment variable needs to be set.")
		.parse::<u16>()
		.expect("Failed to parse SERVER_PORT");
	let client_id = std::env::var("CLIENT_ID")
		.expect("CLIENT_ID environment variable needs to be set.");
	let client_secret = std::env::var("CLIENT_SECRET")
		.expect("CLIENT_SECRET environment variable needs to be set.");

	// Initializing boltz
	let boltz = Boltz::new(&client_id, &client_secret)
		.await
		.unwrap_or_else(move |err| {
			eprintln!("Failed to initialize boltz: {}", err);
			exit(1);
		});

	println!("{:#?}", boltz.token);

	HttpServer::new( move || {
		App::new()
			.wrap(Logger::default())
			.service(index)
	})
		.bind((server_ip, server_port))?
		.run()
		.await
}
