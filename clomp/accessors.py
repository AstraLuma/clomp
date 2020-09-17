"""
Wrapper classes to help access data in commands and components.
"""


class CommandAccessor:
    def __init__(self, cmd):
        self.cmd = cmd

    def name(self):
        return self.cmd.__name__

    def _resolve(self):
        for 

    def components(self):
        ...
