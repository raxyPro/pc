import platform
import psutil
import time
import os

def get_cpu_info():
    """Get and print CPU-related information."""
    print("=== CPU Information ===")
    print(f"Processor: {platform.processor()}")
    print(f"Machine Type: {platform.machine()}")
    print(f"CPU Cores (Logical): {psutil.cpu_count(logical=True)}")
    print(f"CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
    freq = psutil.cpu_freq()
    if freq:
        print(f"CPU Frequency: {freq.current:.2f} MHz")
    else:
        print("CPU Frequency: Not available")

def get_memory_info():
    """Get and print RAM information."""
    print("\n=== Memory Information ===")
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {mem.available / (1024 ** 3):.2f} GB")

def get_cpu_usage(duration=3):
    """Print current CPU usage percentage over a time interval."""
    print("\n=== CPU Usage ===")
    usage = psutil.cpu_percent(interval=duration)
    print(f"CPU Usage over {duration} seconds: {usage}%")

def test_disk_speed(file_name="testfile.tmp", size_mb=100):
    """Test disk read/write speed using a temporary file."""
    print("\n=== Disk Speed Test ===")
    buf = os.urandom(1024 * 1024)  # 1 MB buffer
    
    # Write test
    start_time = time.time()
    with open(file_name, 'wb') as f:
        for _ in range(size_mb):
            f.write(buf)
    write_duration = time.time() - start_time
    
    # Read test
    start_time = time.time()
    with open(file_name, 'rb') as f:
        for _ in range(size_mb):
            f.read(1024 * 1024)
    read_duration = time.time() - start_time
    
    # Clean up test file
    os.remove(file_name)
    
    write_speed = size_mb / write_duration
    read_speed = size_mb / read_duration
    
    print(f"Disk Write Speed: {write_speed:.2f} MB/s")
    print(f"Disk Read Speed: {read_speed:.2f} MB/s")

def get_gpu_info():
    """Detect and print GPU information from NVIDIA, Apple MPS, or AMD GPUs."""
    print("\n=== GPU Information ===")
    # Check NVIDIA GPUs using GPUtil
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            for idx, gpu in enumerate(gpus):
                print(f"GPU {idx}: {gpu.name}, VRAM: {gpu.memoryTotal} MB, Driver: {gpu.driver}")
        else:
            print("No NVIDIA GPUs found via GPUtil.")
    except ImportError:
        print("GPUtil not installed; skipping NVIDIA GPU check.")

    # Check CUDA/MPS using PyTorch
    try:
        import torch
        if torch.cuda.is_available():
            n = torch.cuda.device_count()
            print(f"NVIDIA CUDA device(s) available: {n}")
            for idx in range(n):
                print(f"CUDA GPU {idx}: {torch.cuda.get_device_name(idx)}")
        elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
            print("Apple MPS GPU is available.")
        else:
            print("No CUDA or MPS devices detected by PyTorch.")
    except ImportError:
        print("PyTorch not installed; skipping advanced GPU check.")

    # Basic AMD GPU detection on Linux via lspci
    try:
        import subprocess
        result = subprocess.run(['lspci'], capture_output=True, text=True)
        if "AMD" in result.stdout or "Radeon" in result.stdout:
            print("AMD GPU detected (via lspci).")
    except Exception:
        # Unable to detect AMD GPU on this system or lspci not available
        pass
def print_cpu_clock_speed():
    freq = psutil.cpu_freq()
    if freq:
        print(f"CPU Frequency: Current = {freq.current:.2f} MHz, Min = {freq.min:.2f} MHz, Max = {freq.max:.2f} MHz")
    else:
        print("CPU frequency information not available.")

    # For per-core frequency (if supported)
    freqs = psutil.cpu_freq(percpu=True)
    if freqs:
        for idx, core_freq in enumerate(freqs):
            print(f"Core {idx}: {core_freq.current:.2f} MHz")
    else:
        print("Per-core CPU frequency information not available.")

def main():
    get_cpu_info()
    print_cpu_clock_speed()
    get_memory_info()
    get_cpu_usage()
    test_disk_speed()
    get_gpu_info()

if __name__ == "__main__":
    main()
