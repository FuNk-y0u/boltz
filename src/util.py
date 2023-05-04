class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class util:
    def __init__(self):
        pass
    def log_warning(self, text):
        print(colors.WARNING + "[INFO LOG] " + text)
    
    def log_error(self, text):
        print(colors.FAIL + "[ERROR LOG] " + text)
    
    def log_ok(self, text):
        print(colors.OKGREEN + "[SUCESS LOG] " + text)

    def display_error(self, text):
        print(colors.HEADER + "--=== ERROR CODE ===-- ")
        print(colors.FAIL + text)
        print(colors.HEADER + "--==================-- ")