import os
from time import time
import markdown

print(os.listdir(os.curdir))

file = open('output/index.html', 'w+')
file.write(str(markdown.markdown('#Hi')))
file.close()
