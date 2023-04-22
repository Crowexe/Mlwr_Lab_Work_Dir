import os
import sys
import time
from os import remove

file = open("./malware.txt", "w")
file.write("Primera linea" + os.linesep)
file.write("Segunda linea")
file.close()

time.sleep(5)
remove("./malware.txt")