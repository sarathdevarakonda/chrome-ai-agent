from vapps.package_manager import PackageManager
from vapps.platform_object_types import ICommand, IContextObject, IFrameData, VApp
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ClickCommand(ICommand):
    def do_run(self, ctx, *args):
        if len(args) < 1:
            print("XPath argument is missing.")
            return

        xpath = args[0]
        driver = ctx.get("driver").value
        if driver:
            try:
                element = driver.find_element(By.XPATH,xpath)
                element.click()
                print(f"Clicked element with XPath: {xpath}")
            except Exception as e:
                print(f"exception at {e}")
        else:
            print("WebDriver not found in context store.")


class SendKeysCommand(ICommand):
    def do_run(self, ctx, *args):
        if len(args) < 2:
            print("XPath and keys argument are missing.")
            return

        xpath = args[0]
        keys_to_send = args[1]
        driver = ctx.get("driver").value
        if driver:
            try:
                element = driver.find_element(By.XPATH,xpath)
                element.send_keys(keys_to_send)
                print(f"Sent keys '{keys_to_send}' to element with XPath: {xpath}")
            except Exception as e:
                print(f"Exception: {e}")
        else:
            print("WebDriver not found in context store.")

import time
class SleepCommand(ICommand):
    def do_run(self, ctx, *args):
        time.sleep(2)


class OpenUrlCommand(ICommand):
    def do_run(self, ctx, *args):
        if len(args) < 1:
            return "XPath argument is missing."

        url = args[0]
        driver = ctx.get("driver").value
        print(driver)
        if driver:
            try:
                driver.get(url)
                return driver
            except Exception as e:
                print(e)
                return e
        else:
            return "WebDriver not found in context store."

