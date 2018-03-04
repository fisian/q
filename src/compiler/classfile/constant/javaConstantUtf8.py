from ..javaConstant import JavaConstant
from ..javaTags import constant_tags
from ..util import getByte

class JavaConstantUtf8(JavaConstant):
    def __init__(self, string):
        self.tag = constant_tags['TAG_CONSTANT_UTF8']
        self.utf8String = string
    
    def toBytes(self):
        length = len(self.utf8String)
        return bytes([self.tag, getByte(length, 1), getByte(length, 0)])+self.utf8String.encode('utf-8')
