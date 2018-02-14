import tkinter as tk
from tkinter.constants import BROWSE, SINGLE, END, TOP, BOTTOM, LEFT, RIGHT,\
    DISABLED, NORMAL, VERTICAL, Y, BOTH, INSERT
import re
from machine import MachineState
from liststream import ListStream
from exceptions import QLangException, QLangError

class QDebugFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.initGui()
        code = """
                qqqq qqqqqq 5 qqqq qqq 2
                q q method1begin
                    qqqq qq 1 qqqq qqqqq qqq q - qqqq qqqq qqq q +
                qq q method1end qqq qqq methode1execWHILE
                qqqq qqq qqq q makestring qqqq qqqq qqq q print
        """
        self.program = re.sub(r"[^q ]", "", code).split()
        self.loadCode()
        self.machine = MachineState(debug=True)
    
    def initGui(self):
        self.codeFrame = tk.Frame(self)
        self.codeFrame.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.codeScroll = tk.Scrollbar(self.codeFrame, orient=VERTICAL)
        
        self.codeList = tk.Listbox(self.codeFrame, yscrollcommand=self.codeScroll.set)
        self.codeList.config(selectmode=SINGLE)
        self.codeList.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.codeScroll.config(command=self.codeList.yview)
        self.codeScroll.pack(side=RIGHT, fill=Y)
        
        self.outputFrame = tk.Frame(self)
        self.outputFrame.pack(side=BOTTOM)
        
        self.outputScroll = tk.Scrollbar(self.outputFrame, orient=VERTICAL)
        
        self.outputText = tk.Text(self.outputFrame, yscrollcommand=self.outputScroll.set)
        self.outputText.config(height=10, width=60)
        self.outputText.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.outputScroll.config(command=self.outputText.yview)
        self.outputScroll.pack(side=RIGHT, fill=Y)
        
        self.stackList = tk.Listbox(self)
        self.stackList.config(selectmode=SINGLE)
        self.stackList.pack(side=LEFT)
        
        self.btnFrame = tk.Frame(self)
        self.btnFrame.pack(side=RIGHT, fill=BOTH)
        
        self.stepNextBtn = tk.Button(self.btnFrame)
        self.stepNextBtn.config(text="Step next")
        self.stepNextBtn.config(command=self.stepCode)
        self.stepNextBtn.pack(side=TOP)
        
        self.clearBtn = tk.Button(self.btnFrame)
        self.clearBtn.config(text="Clear output")
        self.clearBtn.config(command=self.clearOutput)
        self.clearBtn.pack(side=TOP)
        
        self.resetBtn = tk.Button(self.btnFrame)
        self.resetBtn.config(text="Reset")
        self.resetBtn.config(command=self.resetCode)
        self.resetBtn.pack(side=TOP)
        
    def loadCode(self):
        if len(self.program)%2 == 0 and len(self.program) > 0:
            for i in range(0, len(self.program), 2):
                self.codeList.insert(END, self.program[i:i+2])
            self.codeList.insert(END, "")
            self.codeList.select_set(0, 0)
        else:
            print("Program must be longer than 0 and length must be divisible by 2")
        
    def stepCode(self):
        current = self.codeList.curselection()
        if len(current) > 0:
            current = current[0]
            with ListStream() as output:
                try:
                    self.machine.eval(self.program[current*2])
                    self.machine.eval(self.program[current*2+1])
                except QLangException as exception:
                    print(exception)
                except QLangError as error:
                    print(error)
                
                self.updateOutput(output)
            
            nextLine = current+1
            if self.codeList.size() > nextLine:
                self.codeList.select_clear(0, END)
                self.codeList.select_set(nextLine, nextLine)
                self.codeList.see(nextLine)
            
            if self.codeList.size() == nextLine+1:
                self.stepNextBtn.config(state=DISABLED)
            
        else:
            print("Nothing selected")
        
    def updateOutput(self, output):
        self.stackList.delete(0, END)
        self.stackList.insert(0, *self.machine.stack)
        self.outputText.insert(END, output.text)
        self.outputText.see(END)
    
    def resetCode(self):
        self.machine = MachineState(debug=True)
        self.codeList.select_clear(0, END)
        self.codeList.select_set(0, 0)
        self.codeList.see(0)
        self.outputText.delete(1.0, END)
        self.stepNextBtn.config(state=NORMAL)
        
    def clearOutput(self):
        self.outputText.delete(1.0, END)

root = tk.Tk()
root.title("QDB")
app = QDebugFrame(root)
app.pack()
app.mainloop()
