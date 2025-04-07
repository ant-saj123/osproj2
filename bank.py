import threading

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

class Teller(threading.Thread):
    def __init__(self, teller_id):
        super().__init__()
        self.teller_id = teller_id

    def run(self):
        print(f"Teller {self.teller_id} ready to serve")

class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id

    def run(self):
        print(f"Customer {self.customer_id} wants to perform a transaction")

for i in range(NUM_TELLERS):
    Teller(i).start()

for i in range(NUM_CUSTOMERS):
    Customer(i).start()
