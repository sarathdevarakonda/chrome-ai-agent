from vapps.platform_object_types import ICommand
from util import to_csv_data
from vapps.vappstore.impl import VappStore

class ListInstalledVApps(ICommand):
    
    def __init__(self) -> None:
        super().__init__()
        self.data = None
    
    def do_run(self, ctx, *args):
                
        data = []
        for app_instance in ctx.get('installed_vapps', {}).items():
            obj = {
                "NAME": app_instance.name,
            }
            data.append(obj)
        self.data = None
        return to_csv_data(headers=["NAME"])