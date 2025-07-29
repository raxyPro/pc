import time
import multiprocessing
import os
import psutil
import socket
from datetime import datetime
from contextlib import redirect_stdout

def cpu_stress_task(n):
    total = 0
    for i in range(n):
        total += (i % 7) * (i % 3)
    return total

def worker_task(n):
    start = time.time()
    result = cpu_stress_task(n)
    elapsed = time.time() - start
    return f"Process {os.getpid()} finished in {elapsed:.4f} seconds. Result: {result}"

def get_cpu_usage_text():
    print("=== CPU Usage ===")
    usage_per_core = psutil.cpu_percent(percpu=True, interval=1)
    for idx, usage in enumerate(usage_per_core):
        print(f"Core {idx}: {usage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%\n")

def main():
    N_ITER = 100_000_000
    NUM_PROCESSES = 4
    NUM_ITERATIONS = 1

    pc_name = socket.gethostname()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pc{pc_name}_threads_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            print(f"System: {pc_name}")
            print(f"Generated at: {datetime.now()}\n")

            get_cpu_usage_text()

            print(f"Running stress test: N_ITER={N_ITER}, NUM_PROCESSES={NUM_PROCESSES}, NUM_ITERATIONS={NUM_ITERATIONS}\n")

            for i in range(1, NUM_ITERATIONS + 1):
                print(f"Iteration {i}/{NUM_ITERATIONS}...")
                start_all = time.time()
                with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
                    results = pool.map(worker_task, [N_ITER] * NUM_PROCESSES)
                total_time = time.time() - start_all

                for res in results:
                    print(res)

                print(f"Total time for iteration {i}: {total_time:.2f} seconds\n")

    print(f"✅ Output saved to {filename}")

if __name__ == "__main__":
    main()
