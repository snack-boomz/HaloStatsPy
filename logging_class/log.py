class Log():
    
    def __init__(self, log_level):
        self.log_level = log_level
    
    def print(self, message, level):
        if self.log_level >= level:
            print(message)
    