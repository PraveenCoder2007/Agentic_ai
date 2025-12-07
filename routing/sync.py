import time

def make_coffee():
    print("Making coffee...")
    time.sleep(3)  # Simulates waiting
    return "Coffee ready"

def make_toast():
    print("Making toast...")
    time.sleep(2)  # Simulates waiting
    return "Toast ready"

# SYNC: One after another
start = time.time()
coffee = make_coffee()    # Wait 3 seconds
toast = make_toast()      # Wait 2 more seconds
print(f"Total time: {time.time() - start:.1f}s")  # 5 seconds
