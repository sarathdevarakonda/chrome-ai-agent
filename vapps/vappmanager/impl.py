from types import VApp
from vapps.vappmanager.context import VappManagerInstance
from vapps.vappmanager.data_commands import ListApps

class VappManagerVapp(VApp):
    def __init__(self):
        super().__init__()    
    
    @property
    def name():
        return "vappmanager"
    