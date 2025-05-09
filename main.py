import threading
import random
import time

# Constants for capacities
OPEN_AREA_CAPACITY = 300
THEATER_CAPACITY = 30

# Visitor priorities
PRIORITIES = ["Gold", "Silver", "Group", "Regular"]

# Shared resources
open_area_count = 0
theater_count = 0
zoo_lock = threading.Lock()

# Visitor queue for each gate
gates = {i: {priority: [] for priority in PRIORITIES} for i in range(1, 4)}

# Add a list to track current visitors
visitors_in_zoo = []

# Modify visitor_thread to track visitors and demonstrate starvation and deadlock
def visitor_thread(gate_id, priority, visiting_option):
    global open_area_count, theater_count, visitors_in_zoo

    visitor_id = f"{priority} visitor at Gate {gate_id} for {visiting_option}"

    # Starvation demonstration: Regular visitors may wait indefinitely
    if priority == "Regular":
        print(f"{visitor_id} is waiting due to higher-priority visitors.")

    with zoo_lock:
        if visiting_option == "Open Area" and open_area_count < OPEN_AREA_CAPACITY:
            open_area_count += 1
            visitors_in_zoo.append(visitor_id)
            print(f"{visitor_id} entered Open Area.")
        elif visiting_option == "Theater" and theater_count < THEATER_CAPACITY:
            theater_count += 1
            visitors_in_zoo.append(visitor_id)
            print(f"{visitor_id} entered Theater.")
        elif visiting_option == "Both":
            # Deadlock demonstration: Acquire locks in different orders
            if random.choice([True, False]):
                with zoo_lock:
                    if open_area_count < OPEN_AREA_CAPACITY:
                        open_area_count += 1
                        if theater_count < THEATER_CAPACITY:
                            theater_count += 1
                            visitors_in_zoo.append(visitor_id)
                            print(f"{visitor_id} entered both Open Area and Theater.")
                        else:
                            open_area_count -= 1
                            print(f"{visitor_id} could not enter Theater due to capacity limits.")
            else:
                with zoo_lock:
                    if theater_count < THEATER_CAPACITY:
                        theater_count += 1
                        if open_area_count < OPEN_AREA_CAPACITY:
                            open_area_count += 1
                            visitors_in_zoo.append(visitor_id)
                            print(f"{visitor_id} entered both Open Area and Theater.")
                        else:
                            theater_count -= 1
                            print(f"{visitor_id} could not enter Open Area due to capacity limits.")
        else:
            print(f"{visitor_id} could not enter {visiting_option} due to capacity limits.")

    time.sleep(random.uniform(0.1, 0.5))  # Simulate time spent in the Zoo

    with zoo_lock:
        if visiting_option == "Open Area":
            open_area_count -= 1
        elif visiting_option == "Theater":
            theater_count -= 1
        elif visiting_option == "Both":
            open_area_count -= 1
            theater_count -= 1
        visitors_in_zoo.remove(visitor_id)
        print(f"{visitor_id} left the Zoo.")

def gate_thread(gate_id):
    while True:
        for priority in PRIORITIES:
            if gates[gate_id][priority]:
                visitor = gates[gate_id][priority].pop(0)
                threading.Thread(target=visitor_thread, args=(gate_id, priority, visitor)).start()
        time.sleep(0.1)  # Simulate gate processing delay

# Add aging mechanism to resolve starvation
def resolve_starvation():
    while True:
        with zoo_lock:
            for gate_id in gates:
                for priority in PRIORITIES[::-1]:  # Reverse order to age lower-priority visitors
                    if gates[gate_id][priority]:
                        visitor = gates[gate_id][priority].pop(0)
                        threading.Thread(target=visitor_thread, args=(gate_id, priority, visitor)).start()
        time.sleep(0.1)  # Simulate processing delay

# Modify simulate_zoo to include starvation resolution
def simulate_zoo():
    # Start gate threads
    for gate_id in gates:
        threading.Thread(target=gate_thread, args=(gate_id,), daemon=True).start()

    # Start starvation resolution thread
    threading.Thread(target=resolve_starvation, daemon=True).start()

    # Simulate visitors arriving at random gates
    while True:
        gate_id = random.randint(1, 3)
        priority = random.choice(PRIORITIES)
        visiting_option = random.choice(["Open Area", "Theater", "Both"])
        gates[gate_id][priority].append(visiting_option)
        print(f"{priority} visitor added to Gate {gate_id} queue for {visiting_option}.")
        time.sleep(random.uniform(0.1, 0.3))

if __name__ == "__main__":
    simulate_zoo()