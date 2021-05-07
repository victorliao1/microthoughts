import os
print(os.listdir(os.curdir))

file = open('output/index.html', 'w+')
file.write("Hello world!")
file.close()
