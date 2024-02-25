from vapps.package_manager import PackageManager
from vapps.platform_object_types import  IContextObject

class WebDriverContextObject(IContextObject):

    
    def _create_value(self):
        chrome_driver = self.webdriver_pkg.webdriver.Chrome()
        return chrome_driver
    
    def __init__(self):
        package_manager = PackageManager()
        self.selenium_pkg = package_manager.get_package('selenium', 'selenium')
        self.webdriver_pkg = package_manager.get_package('selenium', 'selenium.webdriver')
        if not self.selenium_pkg:
            raise Exception("Selenium package is not installed.")
        if not self.webdriver_pkg:
            raise Exception("WebDriver submodule is not available in the Selenium package.")

        self.value = self._create_value()

    def destroy(self):
        if self.value:
            self.value.quit()