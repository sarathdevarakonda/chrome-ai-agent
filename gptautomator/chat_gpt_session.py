from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
class ChatGPTSession:
    def __init__(self, gpt):
        self.messages = []
        self.gpt = gpt
    
    def is_any_conv(self):
        return len(self.gpt.return_chatgpt_conversation()) > 0
    
    def ask(self, prompt):
        self._submit_prompt(prompt['value'])
        timeout = 1  # seconds
        time.sleep(1)
        while True:
            try:
                WebDriverWait(self.gpt.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="send-button"]'))
                )
                return self.gpt.return_last_response()    
            except Exception as e:
                pass
    

    def _submit_prompt(self, value):
        self.gpt.send_prompt_to_chatgpt(value)
        