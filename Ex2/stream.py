import threading
from queue import Queue

class Stream:
    def __init__(self):
        self.queue = Queue()
        self.action = None
        self.next_stream = None
        self.thread = threading.Thread(target=self._run)
        self.running = True
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.thread.start()


    def _run(self):
        while self.running:
            with self.condition:
                while self.queue.empty() or self.action is None:
                    self.condition.wait()
                    if not self.running:
                        return
                item = self.queue.get()
            result = self.action(item)
            if self.next_stream:
                if isinstance(result, bool):
                    if result:
                        self.next_stream.add(item)
                else:
                    self.next_stream.add(result)

    def add(self, x):
        with self.condition:
            self.queue.put(x)
            self.condition.notify()


    def apply(self, func):
        new_stream = Stream()
        self.action = func
        self.next_stream = new_stream
        with self.condition:
            self.condition.notify_all()
        return new_stream


    def forEach(self, func):
        self.action = lambda x: func(x)
        with self.condition:
            self.condition.notify_all()


    def stop(self):
        self.running = False
        with self.condition:
            self.condition.notify_all()
        if self.next_stream:
            self.next_stream.stop()
        self.thread.join()