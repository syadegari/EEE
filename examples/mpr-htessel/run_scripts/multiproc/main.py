import os
import stat

script = '''#!/bin/bash

python program
'''


program = '''import time
import random

pause = 9
for i in range(1, 10):
    print(i)

time.sleep(pause)

if random.random() > 0.80:
    raise Exception(f'quitting the program because of a difficulty')

for i in range(10, 20):
    print(i)

time.sleep(pause + 1)

print('finished executing the program')
'''


num_format = '02'
for i in range(1, 25):
    folder_name = f'folder_{i:02}'
    os.mkdir(f'folder_{i:02}')
    os.chdir(folder_name)
    open('script', 'w').write(script)
    open('program', 'w').write(program)
    st = os.stat('script')
    os.chmod('script', st.st_mode | stat.S_IEXEC)
    st = os.stat('program')
    os.chmod('program', st.st_mode | stat.S_IEXEC)
    os.chdir('..')
