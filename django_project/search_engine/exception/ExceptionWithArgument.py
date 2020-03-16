class ExceptionWithArgument(Exception):
    def __init__(self, msg, *, name):
        self.msg = msg
        self.name = name

    def description(self):
        return f"[thrown {self.name}] {self.msg}"
