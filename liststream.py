import sys

class ListStream:
    def __init__(self):
        self.text = ""
        
    def write(self, s):
        self.text += s
        
    def __enter__(self):
        sys.stdout = self
        return self
        
    def __exit__(self, ext_type, exc_value, traceback):
        sys.stdout = sys.__stdout__
