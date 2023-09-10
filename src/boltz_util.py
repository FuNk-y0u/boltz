from datetime import datetime
from inspect import stack, getframeinfo

# * Boltz color dict
colors:dict = {
    "Info": '\033[95m',
    "Error": '\033[91m',
    "Ok": '\033[92m',
}

# * Boltz logger
def logHeader(text:str) -> None:
    log(text,"Info")
    
def logError(text:str) -> None:
    log(text,"Error")

def logOk(text:str) -> None:
    log(text,"Ok")

def log(message:str,title:str) -> None:
    caller = getframeinfo(stack()[2][0])
    print(f"{colors[title]}{datetime.now()} | {caller.filename}:{caller.lineno} {title} - {message}")