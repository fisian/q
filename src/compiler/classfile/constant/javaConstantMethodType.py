from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantMethodType(JavaConstant):
    def __init__(self, descriptorIndex):
        self.tag = constant_tags['TAG_CONSTANT_METHOD_TYPE']
        self.descriptor_index = descriptorIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.descriptor_index, 1), getByte(self.descriptor_index, 0)])
