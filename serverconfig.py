SERVER_IP = '127.0.0.1'
NGROK_IP = "https://43ef-113-199-226-62.ngrok-free.app"

SERVER_PORT = 80
LOCAL_HOSTING = True

if(LOCAL_HOSTING == True):
    SERVER_LINK = "http://" + SERVER_IP +":"+ str(SERVER_PORT) # for local
else:
    SERVER_LINK = NGROK_IP # for hosting

