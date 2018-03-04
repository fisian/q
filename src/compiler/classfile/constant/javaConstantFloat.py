from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantFloat(JavaConstant):
    def __init__(self, floatBytes):
        self.tag = constant_tags['TAG_CONSTANT_FLOAT']
        self.bytes = floatBytes
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.bytes, 3), getByte(self.bytes, 2), getByte(self.bytes, 1), getByte(self.bytes, 0)])
