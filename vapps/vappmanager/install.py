from vapps.platform_object_types import VApp
from vapps.vappmanager.context import VappManagerInstance
from vapps.vappmanager.data_commands import ListVApps

from vapps.vappmanager.commands import AddVApp
from vapps.platform_object_types import IInstallScript
from vapps.vappmanager.impl import VappManagerVapp
from vapps.vappstore.impl import VappStore

class VappManagerInstallScript(IInstallScript):
    
    def __init__(self) -> None:
        super().__init__()

    def name():
        return "vappmanager"
        
    def initialize(self):
        app = VappManagerVapp()
        manager = VappManagerInstance()
        app.add_context_object("manager", manager)

        app.add_command("d_list_vapps",ListVApps())
        app.add_command("add_vapp",AddVApp())
        return app
