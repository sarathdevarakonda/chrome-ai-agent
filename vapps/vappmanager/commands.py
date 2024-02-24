from vapps.platform_object_types import ICommand
from util import to_csv_data

class AddVApp(ICommand):
    def do_run(self, context_store, *args):
        manager = context_store.get("manager").value
        if not manager:
            print("VappManagerInstance is not available")
            return None
        
        store = manager.get_app('vappstore')
        app_install = store.installed_apps['']
        if app_install.name in manager.apps.items():
            manager.apps[app_install.name] = app_install.install()
            print("add app failed as it exists already")
            return False
        
        return True