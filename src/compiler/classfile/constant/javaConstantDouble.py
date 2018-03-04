from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantDouble(JavaConstant):
    def __init__(self, doubleHighBytes, doubleLowBytes):
        self.tag = constant_tags['TAG_CONSTANT_DOUBLE']
        self.highBytes = doubleHighBytes
        self.lowBytes = doubleLowBytes
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.highBytes, 3), getByte(self.highBytes, 2),\
                      getByte(self.highBytes, 1), getByte(self.highBytes, 0),\
                      getByte(self.lowBytes, 3), getByte(self.lowBytes, 2),\
                      getByte(self.lowBytes, 1), getByte(self.lowBytes, 0)])
