from boltz import *

# * Loading client_id and client_secret for boltz api
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

_boltzController = Boltz(CLIENT_ID, CLIENT_SECRET)
results = _boltzController.search_song("Phonk",BoltzSearchTypes.playlist,50)
for result in results:
    print(result.title + ":" + result.url.id + ":" + str(result.image.url))