import os
print(os.listdir(os.curdir))

file = open('index.html', 'w+')
file.write("Hello world!")
file.close()
