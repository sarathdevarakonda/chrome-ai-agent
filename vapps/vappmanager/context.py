from vapps.platform_object_types import  IContextObject
from package_manager import PackageManager
from objects import VAppManager

class VappManagerInstance(IContextObject):

    
    def _create_value(self):
        manager = VAppManager()
        return manager
    
    def __init__(self):
        self.value = self._create_value()

    def destroy(self):
        pass