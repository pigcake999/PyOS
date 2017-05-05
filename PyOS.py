from sys import *
import os

class System():
    def __init__(self):
        self.bits = "16"
        self.clearAtStart = True
    def setBits(self, bits):
        self.bits = str(bits)


class Term():
    def __init__(self):
        self.prints = []
    def Print(self, string):
        self.prints.append(string)

def Compiler(terminal, system, currentOS):
    if os.path.exists("os"):
        os.system("rd os")
    if os.path.exists("NASM/boot.bin"):
        os.chdir("NASM")
        os.system("del boot.bin")
        os.chdir("..")
    if os.path.exists("os") == False:
        os.system("mkdir os")
    if os.path.exists("os/bootloader.asm") == False:
        if currentOS == "Mac" or currentOS == "Linux":
            os.system("touch os/bootloader.asm")
        elif currentOS == "Windows":
            os.system("echo.>os/bootloader.asm")
    f = open("os/bootloader.asm", "w")

    def newLine(count):
        i = 0
        while(i<count):
            f.write("\n")
            i += 1

    f.write("[BITS "+system.bits+"]\n[org 0x7c00]")

    newLine(2)

    if system.clearAtStart:
        f.write("mov ah, 0x06\nmov al, 0\nint 10h")
        newLine(1)

    i = "a"
    inum = 0
    alphabet = "abcdefghijklmnopqrstubwxyz"
    for string in terminal.prints:
        if string == "\cs":
            f.write("mov ah, 0x06\nmov al, 0\nint 10h")
            newLine(1)
        else:
            if string != "":
                inum += 1
                if inum == len(alphabet):
                    inum = 0
                i += alphabet[inum]
                f.write("mov bx, string_"+i+"\ncall print_string")
                newLine(1)

    """
    Newline Code:
    mov ah, 02h
    mov dl, 13
    int 21h
    mov dl, 10
    int 21h
    ret
    """

    f.write("\njmp $\n\nprint_string:\n\tpusha\n\tmov ah, 0x0e\nprint_loop:\n\tmov al, [bx]\n\tcmp al, 0\n\tje print_string_done\n\tint 0x10\n\tadd bx, 1\n\tjmp print_loop\nprint_string_done:\n\tpopa\n\tret")


    newLine(2)
    i = "a"
    inum = 0
    alphabet = "abcdefghijklmnopqrstubwxyz"
    for string in terminal.prints:
        inum += 1
        if inum == len(alphabet):
            inum = 0
        i += alphabet[inum]
        if string == "\n":
            f.write("string_"+i+" db \"\",13,10,0")
        elif string != "\cs":
            f.write("string_"+i+" db \""+string+"\",0")
        newLine(1)

    newLine(2)

    f.write("times 510 -($-$$) db 0")
    newLine(1)
    f.write("dw 0xaa55")

    f.close()

    if currentOS == "Mac" or currentOS == "Linux":
        os.system("mv os NASM")
    elif currentOS == "Windows":
        os.system("move os NASM")

    if currentOS == "Mac" or currentOS == "Linux":
        os.system("touch os/bootloader.asm")
    elif currentOS == "Windows":
        os.chdir("NASM")
        os.system("nasm.exe os/bootloader.asm -f bin -o boot.bin")

    if currentOS == "Mac" or currentOS == "Linux":
        os.system("cp boot.bin os")
    elif currentOS == "Windows":
        os.system("copy boot.bin os")

    os.system("cd ../")

    os.chdir("..")

    if currentOS == "Mac" or currentOS == "Linux":
        os.system("mv NASM/os .")
    elif currentOS == "Windows":
        os.system("move NASM/os")
