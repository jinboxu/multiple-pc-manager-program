import threading

class MyThread(threading.Thread):
    def __init__(self, name, age):
        super(MyThread, self).__init__()
        self.name = name
        self.age = age

    def run(self):
        while True:
            # event.wait()
            if event.isSet:
                print(info)
            # event.clear()

class Input_fun(threading.Thread):
    def __init__(self):
        super(Input_fun, self).__init__()

    def run(self):
        while True:
            event.clear()
            info = input("input something:").strip()
            if not info:
                continue
            event.set()

event = threading.Event()
event.clear()
info = '12345678'
for i in range(3):
    t = MyThread('jinbo', '27')
    t.start()

c = threading.Thread(target=input_fun, args=())
c.start()