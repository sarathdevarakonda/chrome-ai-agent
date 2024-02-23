import os
import socket
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ChatGPTChrome:

    def __init__(self):
        self.chrome_path = os.getenv('CHROME_PATH')
        self.port = self.find_available_port()  # Use the same port for all sessions
        self.driver = None
        self.chrome_process = None
        self.create_driver()

    def create_driver(self):
        self.quit()  # Make sure any existing WebDriver session is terminated
        self.launch_chrome_with_remote_debugging("https://chat.openai.com")
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver()
        return self.driver

    @staticmethod
    def find_available_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    
    def launch_chrome_with_remote_debugging(self, url):
        chrome_cmd = [self.chrome_path, f'--remote-debugging-port={self.port}', f'--user-data-dir=remote-profile', url]
        self.chrome_process = subprocess.Popen(chrome_cmd)

    def setup_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def return_chatgpt_conversation(self):

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

    def save_conversation(self, file_name):

        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        with open(os.path.join(directory_name, file_name), "a") as file:
            for i in range(0, len(chatgpt_conversation), 2):
                file.write(
                    f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 1].text}\n\n{delimiter}\n\n")


    def return_last_response(self):
        """ :return: the text of the last chatgpt response """
        try:
            response_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.text-base')
            
            if response_elements:
                last_response_element = response_elements[-1]
                
                try:
                    language_elem = last_response_element.find_element(By.CSS_SELECTOR, '[class*="language-"]')
                    return language_elem.text
                except e:
                    return None
        except Exception as e:
            return None
    
    
    def send_prompt_to_chatgpt(self, prompt):
        script = """
            var inputBox = arguments[0];
            inputBox.value = arguments[1];
            inputBox.dispatchEvent(new Event('input', { bubbles: true }));
            inputBox.dispatchEvent(new Event('change', { bubbles: true }));
            """
        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@id, "prompt-textarea")]')
        self.driver.execute_script(script, input_box, prompt)
        input_box.send_keys(Keys.RETURN)


    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")
        while True:
            user_input = input("Enter 'y' if you have completed the log-in or the human verification: ").lower()
            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            else:
                print("Invalid input. Please enter 'y'.")

    def quit(self):
        print("Closing the browser...")
        if self.driver:
            self.driver.quit()
        if self.chrome_process:
            self.chrome_process.terminate()

