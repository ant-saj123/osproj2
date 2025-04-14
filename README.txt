# Bank Simulation Project

## CS4348 Project 2 - Spring 2024

This project simulates a bank with three tellers serving 50 customers. The simulation demonstrates multithreading concepts, including thread synchronization, resource sharing, and semaphores.

## Project Files

- `bank.py` - The main Python script containing the simulation logic

## Requirements

- Python 3.x (This code was tested with Python 3.8+)
- No external libraries are required (only standard library modules)

## How to Run

To run the simulation, open a terminal/command prompt and execute:

```
python3 bank.py
```

## Program Description

### Simulation Overview

This program simulates a bank with the following components:
- 3 tellers who serve customers
- 50 customers who visit the bank to make either deposits or withdrawals
- A bank manager who must approve withdrawals
- A safe that only allows 2 tellers at a time
- A door that allows 2 customers to enter at a time

### Implementation Details

1. **Threading Model**:
   - Each teller and customer is implemented as a separate thread
   - The bank opens when all three tellers are ready
   - Customers enter the bank, perform transactions, and leave

2. **Synchronization Mechanisms**:
   - Semaphores control access to shared resources (safe, manager, door)
   - Events manage the bank's opening and closing
   - Thread-safe queues manage teller availability

3. **Resources and Constraints**:
   - Bank safe: Maximum 2 tellers at once (controlled by `safe_semaphore`)
   - Bank manager: Only 1 teller interaction at a time (controlled by `manager_semaphore`)
   - Bank door: Maximum 2 customers entering at once (controlled by `door_semaphore`)

4. **Workflow**:
   - Tellers announce readiness and wait for customers
   - Customers decide on transactions (deposit or withdrawal) randomly
   - Customers wait in line for an available teller
   - For withdrawals, tellers must get manager approval
   - All transactions require access to the safe
   - Once all customers have been served, the bank closes

## Design Choices and Notes

1. **Thread Communication**:
   - Used individual semaphores for each teller-customer interaction to ensure proper coordination
   - Implemented a ready queue for tellers to avoid busy waiting when possible

2. **Resource Management**:
   - Careful semaphore usage prevents deadlocks
   - Timeouts prevent infinite waiting in case of unexpected issues

3. **Output Format**:
   - The program follows the required output format: `THREAD_TYPE ID [THREAD_TYPE ID]: MSG`
   - Each action is clearly logged with appropriate context



## Known Issues

None identified as of submission.

## Additional Notes for Grader

- The simulation properly implements all requirements from the project specification
- The code includes comments to explain the logic and implementation details
- The implementation uses standard Python threading primitives as specified