dependencies:
	pip install spotify_dl
	pip install youtube_dl
	@echo --=PLEASE INSTALL FFMPEG FROM RESPECTIVE APP STORE OF UR OS--=

powershell:
	$$env:SPOTIPY_CLIENT_ID='0797e2fdf87b42ca8469beae2587bae4'
	$$env:SPOTIPY_CLIENT_SECRET='19fd3eb103e7482587c186b760b8f3c3'

cmd:
	set SPOTIPY_CLIENT_ID='0797e2fdf87b42ca8469beae2587bae4'
	set SPOTIPY_CLIENT_SECRET='19fd3eb103e7482587c186b760b8f3c3'

linux:
	export SPOTIPY_CLIENT_ID='0797e2fdf87b42ca8469beae2587bae4'
	export SPOTIPY_CLIENT_SECRET='19fd3eb103e7482587c186b760b8f3c3'
