import sys
import multiprocessing

def worker(x):
    print('xxxx', x)

def main():
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target = worker)
        jobs.append(p)
        p.start()

if __name__ == '__main__':
    #main()
    """
    o = [worker,'2a',3,'ccc']
    with multiprocessing.Pool(5) as p:
        print(p.map(worker,[o,2,3]))
    """
    p = multiprocessing.Process(target = worker, args=('xx',))
    p.start()
    p.join()

