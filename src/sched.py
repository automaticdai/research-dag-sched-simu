#!/usr/bin/python3
# -*- coding: utf-8 -*-

# DAG Scheduling Simulator
# Xiaotian Dai
# Real-Time Systems Group
# University of York, UK

import os
import logging
import pickle
import json
import random
from pprint import pprint

from task import DAGTask, Task
from processor import Processor


LOG_TO_FILE = False
EXECUTION_MODEL = ["WCET", "BCET", "random", "norm"]
PREEMPTION_COST = 0
MIGRATION_COST = 0


def trace(msglevel, timestamp, message):
    if msglevel == -1: logging.debug("t = " + str(timestamp) + ": " +  message)
    elif msglevel == 0: logging.info("t = " + str(timestamp) + ": " +  message)
    elif msglevel == 1: logging.warning("t = " + str(timestamp) + ": " + message)
    elif msglevel == 2: logging.error("t = " + str(timestamp) + ": " + message)
    else: pass


# random execution
# the processor random pick a task in the ready queue
def random_np():
    t = 0
    T_MAX = 100

    cores = []
    number_of_cores = 2

    for m in range(number_of_cores):
        core = Processor()
        cores.append(core)

    # load taskset
    dag = DAGTask()

    pprint(("V:", dag._V))
    pprint(("E:", dag._E))
    pprint(("Pre:", dag._pre))

    # variables
    finished = False

    w_queue = dag._V.copy() # waitting queue (not released due to constraints)
    r_queue = []            # ready nodes queue
    f_queue = []            # finished nodes queue

    # add the source node
    w_queue.remove(1)
    r_queue.append(1)

    # start scheduling
    trace(0, t, "Started")
    while t < T_MAX and not finished:
        trace(0, t, "Scheduling point reached")

        # update the ready queue (by iterative all left nodes)
        for i in w_queue:
            if all(elem in f_queue  for elem in dag._pre[i]):
                r_queue.append(i)
                w_queue.remove(i)
        
        # iterates all cores
        trace(-1, t, "Check point A")
        for m in range(number_of_cores):
            if cores[m].idle:
                # if anything is in the ready queue
                if r_queue:
                    # randomally pick the next task
                    task_idx = random.choice(r_queue)
                    tau = Task(task_idx, dag._C[task_idx - 1])
                    cores[m].assign(tau)
                    r_queue.remove(task_idx)
                    trace(0, t, "Task {:d} assgined to Core {:d}".format(task_idx, m))

        # check the next scheduling point (the shortest workload time)
        trace(-1, t, "Check point B")
        A_LARGE_NUMBER = 1000000000
        sp = A_LARGE_NUMBER
        for core in cores:
            if core.workload != 0:
                if core.workload < sp:
                    sp = core.workload
        # (the default scheduling point is 1, i.e., check on each tick)
        if sp == A_LARGE_NUMBER:
            sp = 1

        # execute for time sp
        trace(-1, t, "Check point C")
        t = t + sp  # these two statement happens at the same time!
        for m in range(number_of_cores):
            (tau_idx, tau_finished) = cores[m].execute(sp)

            # check finished task and put into the finished queue
            if tau_finished:
                f_queue.append(tau_idx)
                trace(0, t, "Task {:d} finished on Core {:d}".format(tau_idx, m))

        # exit loop if all nodes are finished
        f_queue.sort()
        dag._V.sort()
        if f_queue == dag._V:
            finished = True
    
    makespan = t
    trace(0, t, "Finished: Makespan is {:d}".format(makespan))

    return makespan


def eligibility_np():
    # assign elibility to tasks

    # I. find critical
    # II. find associative tasks
    # III. find non-critical

    # fetch a task

    # assign to a queue
    
    # execution model

    # decide the next scheduling point

    # log result

    pass


if __name__ == "__main__":
    # enable logger
    LOG_FORMAT = '[%(asctime)s-%(levelname)s: %(message)s]'
    LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
    if LOG_TO_FILE == True:
        logging.basicConfig(filename='log.txt', filemode='a', level=logging.INFO,
                            format=LOG_FORMAT, datefmt=LOG_DATEFMT)
    else:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFMT)
    
    random_np()
    #eligibility_np()
