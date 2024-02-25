from vapps.platform_object_types import VApp

from vapps.platform_object_types import VApp

from util import to_csv_data

class VappStore(VApp):
    
    def __init__(self):
        super().__init__()
        self.add_context_object("installed_vapps",{})
        
    def get_installed_vapp(self,name):
        return self.ctx.get("installed_vapps",None).get(name, None)

    def destroy(self):
        return super().destroy()
    
    def name(self):  # Implementation of the abstract method
        return "vappstore"
