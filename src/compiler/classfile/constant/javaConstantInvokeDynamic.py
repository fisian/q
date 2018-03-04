from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantInvokeDynamic(JavaConstant):
    def __init__(self, bootstrapMethodAttrIndex, nameAndTypeIndex):
        self.tag = constant_tags['TAG_CONSTANT_INVOKE_DYNAMIC']
        self.bootstrap_method_attr_index = bootstrapMethodAttrIndex
        self.name_and_type_index = nameAndTypeIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.bootstrap_method_attr_index, 1), getByte(self.bootstrap_method_attr_index, 0),\
                      getByte(self.name_and_type_index, 1), getByte(self.name_and_type_index, 0)])
