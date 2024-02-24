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

    def add_app(self, app):
        if app.name in self.apps:
            print(f"Error: App of type {app.__class__.__name__} already exists.")
        loaded_app = app.install()
        self.apps[app.name] = loaded_app

    def get_app(self, app_id):
        for  app_instance in self.apps.items():
            if app_instance.name == app_id:
                return app_instance
        print(f"Error: App with id {app_id} not found.")
        return None
