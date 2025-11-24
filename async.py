import asyncio
import time
async def make_coffee():
    print("Making coffee...")
    await asyncio.sleep(3)  # Non-blocking wait
    return "Coffee ready"

async def make_toast():
    print("Making toast...")
    await asyncio.sleep(2)  # Non-blocking wait
    return "Toast ready"

# ASYNC: Both at the same time
async def main():
    start = time.time()
    coffee, toast = await asyncio.gather(
        make_coffee(),    # Starts immediately
        make_toast()      # Starts immediately
    )
    print(f"Total time: {time.time() - start:.1f}s")  # 3 seconds

asyncio.run(main())
