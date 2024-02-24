from vapps.package_manager import PackageManager
from vapps.platform_object_types import ICommand
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BodyText(ICommand):
    def do_run(self, context_store, *args):
        driver = context_store.get("driver").value
        if not driver:
            print("WebDriver instance not found in context store.")
            return None
        return driver.execute_script("return document.body.textContent")

class PageTabNavigatedElements(ICommand):
    def __init__(self):
        self.common = None
        self.io_module = None
        self.time_module = None
        self.csv_package = None
        self._initialize_modules()

    def _initialize_modules(self):
        sel = PackageManager().get_package('selenium','selenium.webdriver.common')
        self.common = sel.webdriver.common
        self.by = self.common.by
        self.keys = self.common.keys
        self.io_module = PackageManager().get_package(None,'io')
        self.time_module = PackageManager().get_package(None,'time')
        self.csv_package = PackageManager().get_package(None,'csv')
        self.javascript =  """
            function getElementXPath(elt) {
                var path = "";
                for (; elt && elt.nodeType == 1; elt = elt.parentNode) {
                    var idx = getElementIdx(elt);
                    var xname = elt.tagName;
                    if (idx > 1) xname += "[" + idx + "]";
                    path = "/" + xname + path;
                }
                return path;
            }

            function getElementIdx(elt) {
                var count = 1;
                for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling) {
                    if (sib.nodeType == 1 && sib.tagName == elt.tagName) count++;
                }
                return count;
            }

            return getElementXPath(arguments[0]);
            """


    def do_run(self, context_store, *args):
        
        if not all([self.common, self.io_module, self.time_module, self.csv_package]):
            print("Failed to import necessary modules.")
            return None

        driver = context_store.get("driver").value
        if not driver:
            print("WebDriver instance not found in context store.")
            return None
        initial_element = driver.find_element(self.by.By.TAG_NAME, "body")
        # List to store data related to focused elements
        data = []
        elements = []
        visited_elements = set()
        headers = ['ELEMENT_INDEX', 'TAG', 'TEXT', 'ID', 'NAME', 'INPUT_TYPE', 'VALUE', 'PLACEHOLDER', 'HREF','XPATH']
        for i in range(50):
            self.time_module.sleep(1)
            initial_element.send_keys(self.keys.Keys.TAB)
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
            xpath = "XPATH: "+driver.execute_script(self.javascript, focused_element)
            
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

        initial_element.send_keys(self.keys.Keys.CONTROL + 'l')
        
        return csv_data


class SpecificElementsData(ICommand):
    def __init__(self):
        self.common = None
        self.io_module = None
        self.time_module = None
        self.csv_package = None
        self._initialize_modules()

    def _initialize_modules(self):
        sel = PackageManager().get_package('selenium','selenium.webdriver.common')
        self.common = sel.webdriver.common
        self.by = self.common.by
        self.keys = self.common.keys
        self.io_module = PackageManager().get_package(None,'io')
        self.time_module = PackageManager().get_package(None,'time')
        self.csv_package = PackageManager().get_package(None,'csv')
        self.javascript =  """
            function getElementXPath(elt) {
                var path = "";
                for (; elt && elt.nodeType == 1; elt = elt.parentNode) {
                    var idx = getElementIdx(elt);
                    var xname = elt.tagName;
                    if (idx > 1) xname += "[" + idx + "]";
                    path = "/" + xname + path;
                }
                return path;
            }

            function getElementIdx(elt) {
                var count = 1;
                for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling) {
                    if (sib.nodeType == 1 && sib.tagName == elt.tagName) count++;
                }
                return count;
            }

            return getElementXPath(arguments[0]);
            """


    def do_run(self, context_store, *args):
            
        if not all([self.common, self.io_module, self.time_module, self.csv_package]):
            print("Failed to import necessary modules.")
            return None

        driver = context_store.get("driver").value
        if not driver:
            print("WebDriver instance not found in context store.")
            return None

        initial_element = driver.find_element(self.by.By.TAG_NAME, "body")
        # List to store data related to focused elements
        data = []
        full_data = []
        headers = ['ELEMENT_INDEX', 'TAG', 'TEXT', 'ID', 'NAME', 'INPUT_TYPE', 'VALUE', 'PLACEHOLDER']

        # Define XPath expressions for each type of element
        xpath_expressions = [
            "//input",
            "//a",
            "//select",
            "//option",
            "//button",
            "//form",
            "//textarea",
        ]
        x = 0
        for xpath_expr in xpath_expressions:
            elements = driver.find_elements(self.by.By.XPATH, xpath_expr)
            for i, focused_element in enumerate(elements):
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
                xpath = "XPATH: "+driver.execute_script(self.javascript, focused_element)
                
                obj = {
                    "ELEMENT_INDEX": x,
                    "TAG": tag_name,
                    "TEXT": text,
                    "ID": id,
                    "NAME": name,
                    "VALUE": input_value,
                    "PLACEHOLDER": placeholder,
                    "INPUT_TYPE": input_type,
                }
                
                data.append(obj)
                
                obj['HREF'] = href
                obj['XPATH'] = xpath
                full_data.append(obj)
                x = x + 1

        csv_buffer = self.io_module.StringIO()
        writer = self.csv_package.DictWriter(csv_buffer, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

        # Get CSV data as a string
        csv_data = csv_buffer.getvalue()
        self.full_info = full_data
        self.min_info = data
        return csv_data
