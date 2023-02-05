from vbaProjectCompiler.directory import Directory
from vbaProjectCompiler.vbaProject import VbaProject

def main(args):

def hexDumpString(data):
    decompressed = bytearray(data, encoding="charmap")
    count = 0
    output = ''
    while len(decompressed) > 0:
        output += format(count, 'X').rjust(8, '0') + '   '
        #get 16 Bytes
        stringified = ''
        for i in range(min(16, len(decompressed))):
            char = decompressed.pop(0)
            output += format(char, 'X').rjust(2, '0') + ' '
            sChar = '.' if char < 32 else chr(char)
            stringified += sChar
        output += ' ' + stringified + '\n'
        count += 16
    return output
