import subprocess

class PackageManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.installed_packages = set()
        return cls._instance

    def install_package(self, lib):
        try:
            subprocess.check_call(['pip', "install", lib])
            self.installed_packages.add(lib)
            print(f"Successfully installed package: {lib}")
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install package: {lib}")
            return False

    def get_package(self, lib, package_name):
        
        if lib and lib not in self.installed_packages:
            if not self.install_package(lib):
                return None
        try:
            package = __import__(package_name)
            return package
        except ImportError:
            print(f"Failed to import package: {package_name}")
            return None