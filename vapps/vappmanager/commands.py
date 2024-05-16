from vapps.platform_object_types import ICommand
from util import to_csv_data
from vapps.vapp_store_init import g_vapp_store

class AddVApp(ICommand):
    def do_run(self, ctx, *args):
        app_name = args[0]
        manager = ctx.get("manager").value
        if not manager:
            print("VappManagerInstance is not available")
            return None
        
        print("store")
        InitializeScript = g_vapp_store().get_installed_vapp(app_name)
        print(app_name)
        script_obj = InitializeScript()
        if not InitializeScript:
            print("vapp is not installed")
            return False
        print("Type of manager.apps:", type(manager.apps))

        if app_name in manager.apps:
            print("add app failed as it exists already")
            return False
        
        print(script_obj.name)
        initialize_method = getattr(script_obj, "initialize", None)
        vapp_obj = initialize_method()
        manager.apps[app_name] = vapp_obj

        return True