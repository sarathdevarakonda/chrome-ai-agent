from types import VApp
from vapps.vappmanager.context import VappManagerInstance
from vapps.vappmanager.data_commands import ListApps
from vapps.platform_object_types import VApp

from util import to_csv_data

class VappStore(VApp):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = "vappstore"
            cls._instance.installed_vapps = {}
        return cls._instance
