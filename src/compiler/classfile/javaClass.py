from .constant.javaConstantUtf8 import JavaConstantUtf8
from .constant.javaConstantClass import JavaConstantClass
from .util import getByte
import functools
from compiler.classfile.javaMethod import JavaMethod

class Classfile():
    def __init__(self, classname):
        self.magic = bytes([0xca, 0xfe, 0xba, 0xbe])
        self.minorVersion = bytes([0, 0])
        self.majorVersion = bytes([0, 52]) #Version 52.0: JDK-1.8.0
        self.constantPool = []
        self.accessFlags = bytes([0, 1]) #public
        self.thisClass = bytes([])
        self.superClass = bytes([])
        self.interfacesCount = bytes([0, 0])
        self.interfaces = bytes([])
        self.fieldsCount = bytes([0, 0])
        self.fields = bytes([])
        self.methodsCount = bytes([0, 1])
        self.methods = None
        self.attributesCount = bytes([0, 0])
        self.attributes = bytes([])
        # Add this_class and super_class constants
        this_class_name = self.addConstant(JavaConstantUtf8(classname))
        super_class_name = self.addConstant(JavaConstantUtf8("java/lang/Object"))
        this_class = self.addConstant(JavaConstantClass(this_class_name))
        super_class = self.addConstant(JavaConstantClass(super_class_name))
        # Set this_class and super_class indices
        self.thisClass = bytes([getByte(this_class, 1), getByte(this_class, 0)])
        self.superClass = bytes([getByte(super_class, 1), getByte(super_class, 0)])
        # Add constants for main method
        nameIndex = self.addConstant(JavaConstantUtf8("main"))
        descriptorIndex = self.addConstant(JavaConstantUtf8("([Ljava/lang/String;)V"))
        codeIndex = self.addConstant(JavaConstantUtf8("Code"))
        # Add main method to methods
        self.methods = JavaMethod(nameIndex, descriptorIndex, codeIndex)
    
    # Add constant and return index
    def addConstant(self, constant):
        self.constantPool.append(constant)
        return len(self.constantPool)
    
    def addCodeToMain(self, bytesCode):
        self.methods.appendCode(bytesCode)
    
    def toBytes(self):
        constantPoolCount = len(self.constantPool)+1
        def concatConstants(b1, b2):
            if type(b1) != type(bytes()):
                b1 = b1.toBytes()
            
            return b1+b2.toBytes()
        
        return bytes([])+self.magic+self.minorVersion+self.majorVersion+\
            bytes([getByte(constantPoolCount, 1), getByte(constantPoolCount, 0)])+\
            functools.reduce(lambda b1, b2: concatConstants(b1, b2), self.constantPool)+\
            self.accessFlags+self.thisClass+self.superClass+self.interfacesCount+self.interfaces+\
            self.fieldsCount+self.fields+self.methodsCount+self.methods.toBytes()+\
            self.attributesCount+self.attributes
