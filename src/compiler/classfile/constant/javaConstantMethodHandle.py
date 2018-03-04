from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantMethodHandle(JavaConstant):
    def __init__(self, referenceKind, referenceIndex):
        self.tag = constant_tags['TAG_CONSTANT_METHOD_HANDLE']
        self.reference_kind = referenceKind
        self.reference_index = referenceIndex
    
    def toBytes(self):
        return bytes([self.tag, getByte(self.reference_kind, 0), getByte(self.reference_index, 1), getByte(self.reference_index, 0)])
