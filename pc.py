import platform
import psutil
import time
import os
import subprocess

# Optional modules
try:
    import cpuinfo
except ImportError:
    cpuinfo = None

try:
    import GPUtil
except ImportError:
    GPUtil = None

try:
    import torch
except ImportError:
    torch = None

# ======== CPU Info =========
def get_cpu_info():
    print("=== CPU Information ===")
    if cpuinfo:
        info = cpuinfo.get_cpu_info()
        print(f"Brand: {info.get('brand_raw')}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical Cores: {psutil.cpu_count(logical=True)}")

    freq = psutil.cpu_freq()
    if freq:
        print(f"CPU Frequency: Current = {freq.current:.2f} MHz, Min = {freq.min:.2f} MHz, Max = {freq.max:.2f} MHz")

    print("CPU Usage per Core:")
    for idx, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"  Core {idx}: {usage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# ======== RAM Info =========
def get_ram_info():
    print("\n=== Memory Information ===")
    vm = psutil.virtual_memory()
    print(f"Total RAM: {vm.total / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {vm.available / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {vm.used / (1024 ** 3):.2f} GB")
    print(f"RAM Usage: {vm.percent}%")
    print(f"RAM Speed: {get_ram_speed()} MHz")

def get_ram_speed():
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI()
            for mem in w.Win32_PhysicalMemory():
                return int(mem.Speed)
        elif platform.system() == "Linux":
            result = subprocess.check_output("sudo dmidecode -t memory", shell=True, text=True)
            for line in result.splitlines():
                if "Speed:" in line and "Configured" not in line:
                    return int(line.split(":")[1].strip().split()[0])
    except Exception:
        return "Unavailable"
    return "Unavailable"

# ======== Swap Info =========
def get_swap_info():
    print("\n=== Swap Memory ===")
    swap = psutil.swap_memory()
    print(f"Total Swap: {swap.total / (1024 ** 3):.2f} GB")
    print(f"Used Swap: {swap.used / (1024 ** 3):.2f} GB")
    print(f"Free Swap: {swap.free / (1024 ** 3):.2f} GB")
    print(f"Swap Usage: {swap.percent}%")

# ======== Disk Info =========
def test_disk_speed(file_name="testfile.tmp", size_mb=100):
    print("\n=== Disk Speed Test ===")
    buf = os.urandom(1024 * 1024)

    start_time = time.time()
    with open(file_name, 'wb') as f:
        for _ in range(size_mb):
            f.write(buf)
    write_duration = time.time() - start_time

    start_time = time.time()
    with open(file_name, 'rb') as f:
        for _ in range(size_mb):
            f.read(1024 * 1024)
    read_duration = time.time() - start_time

    os.remove(file_name)
    print(f"Write Speed: {size_mb / write_duration:.2f} MB/s")
    print(f"Read Speed: {size_mb / read_duration:.2f} MB/s")

def get_disk_io():
    print("\n=== Disk I/O Counters ===")
    io = psutil.disk_io_counters()
    print(f"Total Read: {io.read_bytes / (1024 ** 3):.2f} GB")
    print(f"Total Write: {io.write_bytes / (1024 ** 3):.2f} GB")
    print(f"Read Count: {io.read_count}")
    print(f"Write Count: {io.write_count}")

# ======== OS Info =========
def get_os_info():
    print("\n=== OS Information ===")
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.version()}")
    print(f"Release: {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

# ======== Boot Time =========
def get_boot_time():
    print("\n=== Boot Time ===")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time())))

# ======== GPU Info =========
def get_gpu_info():
    print("\n=== GPU Information ===")
    if GPUtil:
        gpus = GPUtil.getGPUs()
        for idx, gpu in enumerate(gpus):
            print(f"GPU {idx}: {gpu.name}, VRAM: {gpu.memoryTotal} MB, Driver: {gpu.driver}")
    else:
        print("GPUtil not installed.")

    if torch:
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                print(f"CUDA GPU {i}: {torch.cuda.get_device_name(i)}")
        elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
            print("Apple MPS GPU is available.")
        else:
            print("No CUDA or MPS GPU available.")
    else:
        print("PyTorch not installed.")

    try:
        result = subprocess.run(['lspci'], capture_output=True, text=True)
        if "AMD" in result.stdout or "Radeon" in result.stdout:
            print("AMD GPU detected (via lspci).")
    except Exception:
        pass

# ======== Main =========
def main():
    get_cpu_info()
    get_ram_info()
    get_swap_info()
    get_disk_io()
    test_disk_speed()
    get_os_info()
    get_boot_time()
    get_gpu_info()

if __name__ == "__main__":
    main()
