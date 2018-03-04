from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantInteger(JavaConstant):
    def __init__(self, intBytes):
        self.tag = constant_tags['TAG_CONSTANT_INTEGER']
        self.bytes = intBytes
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.bytes, 3), getByte(self.bytes, 2), getByte(self.bytes, 1)])
