import sys
import mmap
import ctypes

QLEN = 2048

class Queue(ctypes.Structure):
    _fields_ = [
        ('headIdx', ctypes.c_int),
        ('q', ctypes.c_float * QLEN)
    ]

def print_queue(queue, queLength):
    print(f"headIdx = {queue.headIdx}")
    for i in range(5):
        print(f'Idx: {i} , {queue.q[i]}')

shmem = mmap.mmap(-1, ctypes.sizeof(Queue), 
          "shared_queue")
data = Queue.from_buffer(shmem)
print('Python Program - Getting Data')
print_queue(data,QLEN)
input("Press Enter to continue...")




