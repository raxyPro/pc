import time
import multiprocessing
import os

def cpu_stress_task(n):
    """Simple repeatable CPU-bound calculation."""
    total = 0
    for i in range(n):
        total += (i % 7) * (i % 3)
    return total

def worker_task(n):
    start = time.time()
    result = cpu_stress_task(n)
    elapsed = time.time() - start
    print(f"Process {os.getpid()} finished in {elapsed:.4f} seconds. Result: {result}")
    return elapsed

if __name__ == "__main__":
    N_ITER = 100_000_000  # Number of iterations per process
    NUM_PROCESSES = 8    # Number of processes to run in parallel (match your CPU cores)

    print(f"Running benchmark with {NUM_PROCESSES} parallel processes, each with {N_ITER} iterations...")

    start_all = time.time()
    
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        # Run the worker_task function in parallel processes
        results = pool.map(worker_task, [N_ITER] * NUM_PROCESSES)

    total_elapsed = time.time() - start_all
    print(f"\nAll processes completed in {total_elapsed:.4f} seconds.")
