import threading

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

tellers_semaphore = threading.Semaphore(NUM_TELLERS)

tellers_ready = []
tellers_lock = threading.Lock()

class Teller(threading.Thread):
    def __init__(self, teller_id):
        super().__init__()
        self.teller_id = teller_id

    def run(self):
        print(f"Teller {self.teller_id} ready to serve")
        with tellers_lock:
            tellers_ready.append(self)

class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id

    def run(self):
        tellers_semaphore.acquire()
        with tellers_lock:
            teller = tellers_ready.pop(0)
        print(f"Customer {self.customer_id} selects Teller {teller.teller_id}")
        tellers_semaphore.release()

for i in range(NUM_TELLERS):
    Teller(i).start()

for i in range(NUM_CUSTOMERS):
    Customer(i).start()