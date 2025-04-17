from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor

def func(name):
    for i in range(1000):
        print(name,i)

if __name__ =="__main__":
    with ThreadPoolExecutor(50) as executor:
        for i in range(100):
            executor.submit(func, name=f"线程{i}")
    print("123")

