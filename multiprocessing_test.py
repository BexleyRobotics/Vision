#!/usr/bin/python
import multiprocessing
import time

def getter(q):
    for i in range(30):
        q.put(i);
        time.sleep(1)

def printer(q):
    secs = 0
    while secs < 30:
        secs = q.get(True, 2)
        print secs



queue = multiprocessing.Queue()
get = multiprocessing.Process(target=getter, args=(queue,))
prints = multiprocessing.Process(target=printer, args=(queue,))
get.start()
prints.start()
