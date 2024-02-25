from util import to_csv_data
 
class ManagedVapp:
    def __init__(self, vapp_instance):
        self.vapp = vapp_instance
        self.controller = None

    def get_app_name(self):
        return self.vapp.name

    def get_app_type(self):
        return self.vapp.__class__.__name__


class VAppManager:

    def __init__(self):
        self.apps = {}

    def add_vapp_instance(self, app):
        print(app.name)
        self.apps[app.name()] = app
        
    def add_vapp(self, app):
        if app.name() in self.apps:
            print(f"Error: App of type {app.__class__.__name__} already exists.")
        loaded_app = app.install()
        self.apps[app.name()] = loaded_app

    def get_vapp(self, app_id):
        return self.apps.get(app_id, None)

