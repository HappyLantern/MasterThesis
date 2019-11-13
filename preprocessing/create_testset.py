source = "/home/kevinjohansson1995/final_data"
destination = "/home/kevinjohansson1995/test_data"

import os, shutil, random

data = os.listdir(source)
random.shuffle(data)
data = data[0:int(len(data) * 0.2)]

dir = os.path.join("/home/kevinjohansson1995", "test_data")
if not os.path.exists(dir):
    os.mkdir(dir)
    
    
for i in range(len(data)):
    shutil.move(os.path.join(source, data[i]), os.path.join(destination, data[i]))