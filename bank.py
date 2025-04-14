import threading
import time
import random


# Constants
NUM_TELLERS = 3
NUM_CUSTOMERS = 50


# Semaphores and shared resources
bank_open = threading.Event()
tellers_done = threading.Event()
door_semaphore = threading.Semaphore(2)
safe_semaphore = threading.Semaphore(2)
manager_semaphore = threading.Semaphore(1)


# Tellers ready queue
tellers_ready = []
tellers_ready_lock = threading.Lock()


# Track completed customers
completed_customers = 0
completed_lock = threading.Lock()


class Teller(threading.Thread):
   def __init__(self, teller_id):
       super().__init__()
       self.teller_id = teller_id
       self.customer_ready = threading.Semaphore(0)
       self.transaction_ready = threading.Semaphore(0)
       self.transaction_done = threading.Semaphore(0)
       self.customer_done = threading.Semaphore(0)
       self.current_customer = None
       self.daemon = True


   def run(self):
       print(f"Teller {self.teller_id} []: ready to serve")
       print(f"Teller {self.teller_id} []: waiting for a customer")
       with tellers_ready_lock:
           tellers_ready.append(self)


       bank_open.set()


       while not tellers_done.is_set():
           if not self.customer_ready.acquire(timeout=0.1):
               continue


           customer = self.current_customer
           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: serving a customer")
           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: asks for transaction")


           self.transaction_ready.acquire()
           transaction = customer.transaction


           if transaction == 'Withdrawal':
               print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: going to the manager")
               manager_semaphore.acquire()
               print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: getting manager's permission")
               time.sleep(random.uniform(0.005, 0.03))
               print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: got manager's permission")
               manager_semaphore.release()


           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: going to safe")
           safe_semaphore.acquire()
           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: enter safe")
           time.sleep(random.uniform(0.01, 0.05))
           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: leaving safe")
           safe_semaphore.release()


           print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: finishes {transaction.lower()} transaction.")
           self.transaction_done.release()
           self.customer_done.acquire()


           with completed_lock:
               global completed_customers
               completed_customers += 1
               if completed_customers >= NUM_CUSTOMERS:
                   tellers_done.set()


           print(f"Teller {self.teller_id} []: ready to serve")
           print(f"Teller {self.teller_id} []: waiting for a customer")


       print(f"Teller {self.teller_id} []: leaving for the day")


class Customer(threading.Thread):
   def __init__(self, customer_id):
       super().__init__()
       self.customer_id = customer_id
       self.transaction = random.choice(['Deposit', 'Withdrawal'])


   def run(self):
       print(f"Customer {self.customer_id} []: wants to perform a {self.transaction.lower()} transaction")
       time.sleep(random.uniform(0, 0.1))


       door_semaphore.acquire()
       print(f"Customer {self.customer_id} []: entering bank.")
       print(f"Customer {self.customer_id} []: getting in line.")


       while True:
           with tellers_ready_lock:
               if tellers_ready:
                   teller = tellers_ready.pop(0)
                   break
           time.sleep(0.01)


       teller.current_customer = self
       print(f"Customer {self.customer_id} [Teller {teller.teller_id}]: selects teller")
       print(f"Customer {self.customer_id} [Teller {teller.teller_id}] introduces itself")
       teller.customer_ready.release()


       print(f"Customer {self.customer_id} [Teller {teller.teller_id}]: asks for {self.transaction.lower()} transaction")
       teller.transaction_ready.release()


       teller.transaction_done.acquire()
       print(f"Customer {self.customer_id} [Teller {teller.teller_id}]: leaves teller")
       teller.customer_done.release()


       print(f"Customer {self.customer_id} []: goes to door")
       print(f"Customer {self.customer_id} []: leaves the bank")
       door_semaphore.release()


       with tellers_ready_lock:
           tellers_ready.append(teller)


def main():
   tellers = [Teller(i) for i in range(NUM_TELLERS)]
   for t in tellers:
       t.start()


   bank_open.wait()


   customers = [Customer(i) for i in range(NUM_CUSTOMERS)]
   for c in customers:
       c.start()


   for c in customers:
       c.join()


   tellers_done.set()


   for t in tellers:
       t.join()


   print("The bank closes for the day.")


if __name__ == "__main__":
   main()
