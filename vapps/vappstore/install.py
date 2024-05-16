from vapps.vappstore.impl import VappStore
from vapps.platform_object_types import IInstallScript
from vapps.vappstore.data_commands import ListInstalledVApps
from vapps.vappstore.commands import InstallVapp

class VappStoreInstallScript(IInstallScript):
    
    def __init__(self) -> None:
        super().__init__()
        
    def name():
        return "vappstore"
    
    def initialize(self):
        app = VappStore()
        app.add_command("d_list_installed_apps",ListInstalledVApps())
        app.add_command("install",InstallVapp())
        return app