from vapps.platform_object_types import ICommand
from util import to_csv_data

class ListVApps(ICommand):
    def do_run(self, context_store, *args):
        manager = context_store.get("manager").value
        if not manager:
            print("VappManager instance not found in context store.")
            return None
        
        data = []
        for app_instance in self.apps.items():
            obj = {
                "NAME": app_instance.name,
                "ID": app_instance.name,
                "CONTROLLER" : app_instance.controller
            }
            data.append(obj)
        
        return to_csv_data(headers=["NAME","ID","CONTROLLER"])