import os
from time import time
print(os.listdir(os.curdir))

file = open('index.html', 'w+')
file.write("Hello world!")
file.write(str(time()))
file.close()
