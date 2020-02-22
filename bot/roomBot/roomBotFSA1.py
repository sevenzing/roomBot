from . import config


class roomBot:

    def __init__(self, state):
        """
        States:
            0 - without building
            1 - with building
            2 - listen for buy list
        """

        self.state = state
    
    def action(self, command: str):
        if command == '/help':
            return config.HELP_MESSAGE
        
        if self.state == 0:
            