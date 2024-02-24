from vapps.chrome.impl import ChromeVapp
from vapps.chrome.context import WebDriverContextObject
from vapps.chrome.commands import ClickCommand, OpenUrlCommand, SleepCommand, SendKeysCommand
from vapps.chrome.data_commands import PageTabNavigatedElements, SpecificElementsData, BodyText
from vapps.platform_object_types import IInstallScript

class ChromeInstallScript(IInstallScript):
    def __init__(self) -> None:
        super().__init__()
    
    @property    
    def name():
        return ChromeVapp.name
        
    def intialize(self):
        app = ChromeVapp()
        app.add_context_object("driver", WebDriverContextObject())
        
        app.add_command("open_url",OpenUrlCommand())
        app.add_command("click",ClickCommand())
        app.add_command("send_keys", SendKeysCommand())
        app.add_command("sleep", SleepCommand())
        
        app.add_command("d_tab_navigated_elements",PageTabNavigatedElements())
        app.add_command("d_specific_elements",SpecificElementsData())
        app.add_framadd_commande_data("d_body_text",BodyText())
        return app
