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
        self.ctx = {}
        self.command_store = {}
        self.frame_data_store = {}

    @abc.abstractmethod
    def name(self):
        return "NO NAME"
    
    @abc.abstractmethod
    def destroy(self):
        pass
        
    def execute_commands(self, commands):
        for command_data in commands:
            if not command_data:
                continue
            command_name = command_data[0]
            command_args = command_data[1:]
            command = self.get_command(command_name)
            print(command)
            if command:
                command.do_run(self.ctx, *command_args)
            else:
                print(f"Command '{command_name}' not found.")

    def get_command(self, key):
        return self.command_store.get(key)

    def get_frame_data(self, key):
        f_data =  self.frame_data_store.get(key)
        return f_data.get_frame_data(self.ctx)
    
    def add_command(self, key, command):
        self.command_store[key] = command

    def add_frame_data(self, key, frame_data_handler):
        self.frame_data_store[key] = frame_data_handler
        
    def add_context_object(self, key, context_object):
        self.ctx[key] = context_object
    
    def remove_context_object(self, key):
        self.ctx[key].destroy()
        del self.ctx[key]

class IContextObject(abc.ABC):
    def __init__(self):
        self.value = self._create_value()

    @abc.abstractmethod
    def _create_value(self):
        pass

    def get_value(self):
        return self.value

class IInstallScript(abc.ABC):
    @abc.abstractmethod
    def initialize(self):
        """
        Abstract method to install a VApp.
        """
        pass
    @abc.abstractmethod
    def name(self):
        pass
