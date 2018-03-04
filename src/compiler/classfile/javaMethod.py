from .util import getByte

class JavaMethod():
    def __init__(self, nameIndex, descriptorIndex, codeIndex):
        self.access_flags = bytes([0, 9]) #public static
        self.name_index = bytes([getByte(nameIndex, 1), getByte(nameIndex, 0)])
        self.descriptor_index = bytes([getByte(descriptorIndex, 1), getByte(descriptorIndex, 0)])
        self.code_index = codeIndex
        self.code = bytes([])
        self.max_stack = 9999
        self.max_locals = 1
    
    def appendCode(self, bytesCode):
        self.code = self.code+bytesCode
    
    def toBytes(self):
        attributes_count = bytes([0, 1])
        codeLength = len(self.code)
        attrLength = codeLength+12
        attributes = bytes([getByte(self.code_index, 1), getByte(self.code_index, 0),\
                            getByte(attrLength, 3), getByte(attrLength, 2),\
                            getByte(attrLength, 1), getByte(attrLength, 0),\
                            getByte(self.max_stack, 1), getByte(self.max_stack, 0),\
                            getByte(self.max_locals, 1), getByte(self.max_locals, 0),\
                            getByte(codeLength, 3), getByte(codeLength, 2),\
                            getByte(codeLength, 1), getByte(codeLength, 0)])+\
                            self.code+\
                            bytes([0, 0, 0, 0])
        return self.access_flags+self.name_index+self.descriptor_index+attributes_count+attributes
