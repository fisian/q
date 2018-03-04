from .classfile.javaClass import Classfile
from compiler.classfile.bytecode import bytecode_return, bytecode_goto,\
    bytecode_invokestatic, bytecode_getstatic, bytecode_invokevirtual
from .classfile.util import getByte
from compiler.classfile.constant.javaConstantUtf8 import JavaConstantUtf8
from compiler.classfile.constant.javaConstantNameAndType import JavaConstantNameAndType
from compiler.classfile.constant.javaConstantFieldref import JavaConstantFieldref
from compiler.classfile.constant.javaConstantClass import JavaConstantClass
from compiler.classfile.constant.javaConstantMethodref import JavaConstantMethodref

if __name__ == '__main__':
    javaClassFile = Classfile("q_lang")
    system_name_index = javaClassFile.addConstant(JavaConstantUtf8("java/lang/System")) #8
    printstream_name_index = javaClassFile.addConstant(JavaConstantUtf8("java/io/PrintStream")) #9
    printstream_type_name_index = javaClassFile.addConstant(JavaConstantUtf8("Ljava/io/PrintStream;")) #10
    out_name_index = javaClassFile.addConstant(JavaConstantUtf8("out")) #11
    out_type_name_and_type_index = javaClassFile.addConstant(JavaConstantNameAndType(out_name_index, printstream_type_name_index)) #12
    system_class_index = javaClassFile.addConstant(JavaConstantClass(system_name_index)) #18
    system_out_fieldref_index = javaClassFile.addConstant(JavaConstantFieldref(system_class_index, out_type_name_and_type_index)) #13
    printstream_class_index = javaClassFile.addConstant(JavaConstantClass(printstream_name_index)) #19
    println_name_index = javaClassFile.addConstant(JavaConstantUtf8("println")) #15
    void_name_index = javaClassFile.addConstant(JavaConstantUtf8("()V")) #14
    println_name_and_type_index = javaClassFile.addConstant(JavaConstantNameAndType(println_name_index, void_name_index)) #16
    println_methodref_index = javaClassFile.addConstant(JavaConstantMethodref(printstream_class_index, println_name_and_type_index)) #17
    bytecode = bytes([bytecode_getstatic, getByte(system_out_fieldref_index, 1), getByte(system_out_fieldref_index, 0),\
                      bytecode_invokevirtual, getByte(println_methodref_index, 1), getByte(println_methodref_index, 0)])
    javaClassFile.addCodeToMain(bytecode)
    javaClassFile.addCodeToMain(bytes([bytecode_return]))
    with open("q_lang.class", 'bw') as binfile:
        binfile.write(javaClassFile.toBytes())
    
else:
    print(__name__)