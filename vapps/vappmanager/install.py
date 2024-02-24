from types import VApp
from vapps.vappmanager.context import VappManagerInstance
from vapps.vappmanager.data_commands import ListVApps

from vapps.vappmanager.commands import AddVApp
from vapps.platform_object_types import IInstallScript
from vapps.vappmanager.impl import VappManagerVapp
from vapps.vappstore.impl import VappStore

class VappManagerInstallScript(IInstallScript):
    
    def __init__(self) -> None:
        super().__init__()

    @property
    def name():
        return VappManagerVapp.name
        
    def intialize(self):
        app = VappManagerVapp(self.name)
        manager = VappManagerInstance()
        manager.value.add_app(VappStore())
        app.add_context_object("manager", VappManagerInstance())

        app.add_command("d_list_apps",ListVApps())
        app.add_command("add_app",AddVApp())
        return app
