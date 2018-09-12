"""
进程队列测试：

关闭子进程任务

"""


import time

from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print ('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    # time.sleep(random.random() * 30)
    time.sleep(60)
    end = time.time()
    print ('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print ('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(20):
        p.apply_async(long_time_task, args=(i,))
        time.sleep(0.1)
    print ('Waiting for all subprocesses done...')

    print ("asdfasdf")
    p.close()
    p.join()
    print ('All subprocesses done.')





# from multiprocessing import Process
#
# def run_forever():
#     while 1:
#         print(time.time())
#         time.sleep(2)
#
# def main():
#     p = Process(target=run_forever)
#     p.start()
#     print('start a process.')
#     time.sleep(10)
#     if p.is_alive:
#         # stop a process gracefully
#         p.terminate()
#         print('stop process')
#         p.join()
#
#
# if __name__ == '__main__':
#     main()
