from vapps.platform_object_types import ICommand

class InstallVapp(ICommand):
    def do_run(self, ctx, *args):
        install_script = args[0]
        if install_script.name() in ctx.get('installed_vapps',None):
            print(f"Error: VApp {install_script.name()} is already installed.")
            return

        installed_vapps = ctx.get('installed_vapps', None)
        if installed_vapps is not None:
            installed_vapps[install_script.name()] = install_script
            print(f"{install_script.name()} installed successfully.")
            return True

        
        return False