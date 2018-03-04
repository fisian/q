from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantClass(JavaConstant):
    def __init__(self, nameIndex):
        self.tag = constant_tags['TAG_CONSTANT_CLASS']
        self.name_index = nameIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.name_index, 1), getByte(self.name_index, 0)])
