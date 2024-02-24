


from types import VApp

class ChromeVapp(VApp):
    def __init__(self):
        super().__init__()
    
    @property
    def name():
        return "chrome"