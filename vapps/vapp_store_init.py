from vapps.vappstore.install import VappStoreInstallScript

def create_read_only(value):
    def get_value():
        return value
    return get_value


g_vapp_store = create_read_only(VappStoreInstallScript().initialize())


def create_vapp_manager():
   
    vapp_manager_install_script = g_vapp_store().ctx.get('installed_vapps', {}).get('vappmanager')
    g_vapp_manager = None
    if vapp_manager_install_script:
        # Instantiate the class object if it's a class
        vapp_manager_script = vapp_manager_install_script()  # Instantiate if it's a class
        # Call the initialize method if it exists
        initialize_method = getattr(vapp_manager_script, "initialize", None)
        if callable(initialize_method):
            g_vapp_manager = initialize_method()
        else:
            print("initialize method not found or not callable")     
    else:
        print("VappManagerInstallScript class name not found in installed_vapps")

    return g_vapp_manager