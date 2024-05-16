from vapps.platform_object_types import VApp

class VappManagerVapp(VApp):
    def __init__(self):
        super().__init__()    
    
    @property
    def name():
        return "vappmanager"
    
    def destroy(self):
        return super().destroy()