from .javaTags import constant_tags

class JavaConstant():
    def __init__(self):
        self.tag = constant_tags['TAG_CONSTANT_DEFAULT']
        self.info = []
    
    def toBytes(self):
        return bytes([self.tag]+self.info)
