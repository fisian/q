from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantNameAndType(JavaConstant):
    def __init__(self, nameIndex, descriptorIndex):
        self.tag = constant_tags['TAG_CONSTANT_NAME_AND_TYPE']
        self.name_index = nameIndex
        self.descriptor_index = descriptorIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.name_index, 1), getByte(self.name_index, 0),\
                      getByte(self.descriptor_index, 1), getByte(self.descriptor_index, 0)])
