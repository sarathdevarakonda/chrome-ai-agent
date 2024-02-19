import subprocess

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
        if lib not in self.installed_packages:
            if not self.install_package(lib):
                return None
        try:
            package = __import__(package_name)
            return package
        except ImportError:
            print(f"Failed to import package: {package_name}")
            return None


import abc

class ICommand(abc.ABC):
    @abc.abstractmethod
    def do_run(self, vapp_context, *args):
        pass

class IFrameData(abc.ABC):
    @abc.abstractmethod
    def get_frame_data(self, vapp_context):
        pass

class VApp(abc.ABC):
    def __init__(self):
        self.context_store = {}
        self.command_store = {}
        self.frame_data_store = {}

    def execute_commands(self, commands):
        for command_data in commands:
            if not command_data:
                continue
            command_name = command_data[0]
            command_args = command_data[1:]
            command = self.get_command(command_name)
            if command:
                command.do_run(self.context_store, *command_args)
            else:
                print(f"Command '{command_name}' not found.")

    def get_context(self, key):
        return self.context_store.get(key)

    def get_command(self, key):
        return self.command_store.get(key)

    def get_frame_data_handler(self, key):
        return self.frame_data_store.get(key)
    
    def add_command(self, key, command):
        self.command_store[key] = command

    def add_frame_data(self, key, frame_data_handler):
        self.frame_data_store[key] = frame_data_handler
        
    def add_context_object(self, key, context_object):
        self.context_store[key] = context_object
    
    def remove_context_object(self, key):
        self.context_store[key].destroy()
        del self.context_store[key]

class IContextObject(abc.ABC):
    def __init__(self):
        self.value = self._create_value()

    @abc.abstractmethod
    def _create_value(self):
        pass

    def get_value(self):
        return self.value

class ChromeVapp(VApp):
    def __init__(self):
        super().__init__()

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


from selenium.common.exceptions import NoSuchElementException

class ClickCommand(ICommand):
    def do_run(self, context_store, *args):
        if len(args) < 1:
            print("XPath argument is missing.")
            return

        xpath = args[0]
        driver = context_store.get("driver")
        if driver:
            try:
                element = driver.find_element(xpath)
                element.click()
                print(f"Clicked element with XPath: {xpath}")
            except NoSuchElementException:
                print(f"Element with XPath {xpath} not found.")
        else:
            print("WebDriver not found in context store.")

class PageTabNavigatedElements(IFrameData):
    def __init__(self):
        self.by_module = None
        self.keys_module = None
        self.io_module = None
        self.time_module = None
        self.csv_package = None

    def _initialize_modules(self):
        self.by_module = PackageManager().get_package('selenium.webdriver.common.by')
        self.keys_module = PackageManager().get_package('selenium.webdriver.common.keys')
        self.io_module = PackageManager().get_package('io')
        self.time_module = PackageManager().get_package('time')
        self.csv_package = PackageManager().get_package('csv')

    def get_frame_data(self, context_store):
        if not all([self.by_module, self.keys_module, self.io_module, self.time_module, self.csv_package]):
            print("Failed to import necessary modules.")
            return None

        driver = context_store.get("webdriver")
        if not driver:
            print("WebDriver instance not found in context store.")
            return None

        self._initialize_modules()

        prev_focused_element = None
        initial_element = driver.find_element(self.by_module.TAG_NAME, "body")
        # List to store data related to focused elements
        data = []
        elements = []
        visited_elements = set()
        
        headers = ['ELEMENT_INDEX', 'TAG', 'TEXT', 'ID', 'NAME', 'INPUT_TYPE', 'VALUE', 'PLACEHOLDER', 'HREF', 'XPATH']
        for i in range(50):
            self.time_module.sleep(1)
            initial_element.send_keys(self.keys_module.TAB)
            # Get the currently focused element
            focused_element = driver.switch_to.active_element
            elements.insert(i, focused_element)
            # Extract relevant information
            tag_name = focused_element.tag_name
            class_name = focused_element.get_attribute("class")
            input_value = focused_element.get_attribute("value")
            id = focused_element.get_attribute("id")
            placeholder = focused_element.get_attribute("placeholder")
            name = focused_element.get_attribute("name")
            text = focused_element.text if tag_name != "body" else None
            input_type = focused_element.get_attribute("type") if tag_name == "input" else None
            href = focused_element.get_attribute("href") if tag_name == "a" else None
            xpath = driver.execute_script("return arguments[0].getXPath();", focused_element)  # Assuming getXPath() method is available
            
            data.append({
                "ELEMENT_INDEX": i,
                "TAG": tag_name,
                "TEXT": text,
                "ID": id,
                "NAME": name,
                "VALUE": input_value,
                "PLACEHOLDER": placeholder,
                "INPUT_TYPE": input_type,
                "HREF": href,
                "XPATH": xpath
            })
            text_small = focused_element.text[:10] if tag_name != "body" else None
            element_identifier = (tag_name, id, text_small, class_name)
            if element_identifier in visited_elements:
                break  # Exit loop if the element has been visited before
            else:
                visited_elements.add(element_identifier)

        csv_buffer = self.io_module.StringIO()
        writer = self.csv_package.DictWriter(csv_buffer, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

        # Get CSV data as a string
        csv_data = csv_buffer.getvalue()

        initial_element.send_keys(self.keys_module.CONTROL + 'l')
        
        return csv_data


chrome_vapp = ChromeVapp()
chrome_vapp.add_context_object("driver", WebDriverContextObject())

while(True):
    name = input("Exit: ")
    if 'y' in name:
        chrome_vapp.remove_context_object('driver')
        break