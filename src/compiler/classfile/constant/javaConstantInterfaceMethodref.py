from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantInterfaceMethodref(JavaConstant):
    def __init__(self, classIndex, nameAndTypeIndex):
        self.tag = constant_tags['TAG_CONSTANT_INTERFACE_METHODREF']
        self.class_index = classIndex
        self.name_and_type_index = nameAndTypeIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.class_index, 1), getByte(self.class_index, 0),\
                      getByte(self.name_and_type_index, 1), getByte(self.name_and_type_index, 0)])
