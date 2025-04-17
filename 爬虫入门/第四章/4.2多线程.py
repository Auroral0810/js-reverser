from threading import Thread

def func():
    for i in range(1000):
        print("func",i)
if __name__ == '__main__':
    t = Thread(target=func)
    t.start()
    for i in range(1000):
        print("main",i)