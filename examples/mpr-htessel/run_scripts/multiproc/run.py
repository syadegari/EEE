from subprocess import Popen, PIPE
import os
import time

for i in range(1, 17):
    folder_name = f'folder_{i:02}'
    os.chdir(folder_name)
    t1 = time.time()
    p = Popen(['./script'], stdout=open('output', 'w'), stderr=open('error', 'w')).communicate()
    t2 = time.time()
    open('output', 'w').write(f'runetime took {t2 - t1} seconds')
    os.chdir('..')
