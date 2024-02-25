


from vapps.platform_object_types import VApp

class ChromeVapp(VApp):
    def __init__(self):
        super().__init__()
    
    @property
    def name():
        return "chrome"
    
    def destroy(self):
        return super().destroy()