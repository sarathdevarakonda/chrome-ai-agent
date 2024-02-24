from vapps.platform_object_types import ICommand
from util import to_csv_data
from vapps.vappstore.impl import VappStore

class InstallVapp(ICommand):
    def do_run(self, context_store, *args):
        vapp_store = VappStore()
        install_script = args[0]
        if install_script.name in vapp_store.installed_vapps:
            print(f"Error: VApp {install_script.name} is already installed.")
            return

        self.installed_vapps[install_script.name] = install_script
        print(f"{install_script.name} installed successfully.")
        
        return True