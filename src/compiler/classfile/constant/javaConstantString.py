from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantString(JavaConstant):
    def __init__(self, stringIndex):
        self.tag = constant_tags['TAG_CONSTANT_STRING']
        self.string_index = stringIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.string_index, 1), getByte(self.string_index, 0)])
