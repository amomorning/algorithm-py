import threading
import time
import queue

Q = queue.Queue(4)


def worker():
    while True:
        item = Q.get()
        print(f'Working on {item}')
        time.sleep(1)
        print(f'Finished {item}')
        Q.task_done()

def main():
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    for item in range(10):
        if (Q.full()):
            print('\033[91m', end='')
            print(f'Queue is full, {item} is waiting...\033[0m')
        Q.put(item)
        print('\033[92m', end='')
        print(f'Queueing {item} \033[0m')

    Q.join()
    worker_thread.join()

if __name__ == '__main__':
    main()
