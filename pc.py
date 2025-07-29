import platform
import psutil
import subprocess
import os
import time
from datetime import datetime
import socket

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

html_output = []

def log_html(title, content):
    html_output.append(f"<h2>{title}</h2><pre>{content}</pre>")

def get_cpu_spec():
    content = ""
    if cpuinfo:
        info = cpuinfo.get_cpu_info()
        content += f"Brand: {info.get('brand_raw')}\n"
    content += f"Architecture: {platform.machine()}\n"
    content += f"Processor: {platform.processor()}\n"
    content += f"Physical Cores: {psutil.cpu_count(logical=False)}\n"
    content += f"Logical Cores: {psutil.cpu_count(logical=True)}\n"
    freq = psutil.cpu_freq()
    if freq:
        content += f"CPU Frequency: Min = {freq.min:.2f} MHz, Max = {freq.max:.2f} MHz"
    log_html("CPU Specifications", content)

def get_ram_spec():
    content = ""
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI()
            for mem in w.Win32_PhysicalMemory():
                content += f"RAM Speed: {mem.Speed} MHz\n"
        elif platform.system() == "Linux":
            result = subprocess.check_output("sudo dmidecode -t memory", shell=True, text=True)
            for line in result.splitlines():
                if "Speed:" in line and "Configured" not in line:
                    content += f"RAM Speed: {line.split(':')[1].strip()}\n"
                    break
        else:
            content += "RAM speed: Unsupported OS\n"
    except Exception:
        content += "RAM Speed: Unavailable\n"
    log_html("RAM Specifications", content)

def get_gpu_spec():
    content = ""
    if GPUtil:
        gpus = GPUtil.getGPUs()
        for idx, gpu in enumerate(gpus):
            content += f"GPU {idx}: {gpu.name}, VRAM: {gpu.memoryTotal} MB, Driver: {gpu.driver}\n"
    else:
        content += "GPUtil not installed.\n"

    if torch:
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                content += f"CUDA GPU {i}: {torch.cuda.get_device_name(i)}\n"
        elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
            content += "Apple MPS GPU is available.\n"
        else:
            content += "No CUDA or MPS GPU available.\n"
    else:
        content += "PyTorch not installed.\n"

    try:
        result = subprocess.run(['lspci'], capture_output=True, text=True)
        if "AMD" in result.stdout or "Radeon" in result.stdout:
            content += "AMD GPU detected (via lspci).\n"
    except Exception:
        pass

    log_html("GPU Specifications", content)

def get_os_spec():
    content = ""
    content += f"OS: {platform.system()}\n"
    content += f"Version: {platform.version()}\n"
    content += f"Release: {platform.release()}\n"
    content += f"Machine: {platform.machine()}\n"
    content += f"Processor: {platform.processor()}\n"
    log_html("OS Information", content)

def get_cpu_usage():
    content = "CPU Usage per Core:\n"
    for idx, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        content += f"  Core {idx}: {usage}%\n"
    content += f"Total CPU Usage: {psutil.cpu_percent()}%"
    log_html("CPU Usage", content)

def get_ram_usage():
    vm = psutil.virtual_memory()
    content = (
        f"Total RAM: {vm.total / (1024 ** 3):.2f} GB\n"
        f"Available RAM: {vm.available / (1024 ** 3):.2f} GB\n"
        f"Used RAM: {vm.used / (1024 ** 3):.2f} GB\n"
        f"RAM Usage: {vm.percent}%"
    )
    log_html("RAM Usage", content)

def get_swap_usage():
    swap = psutil.swap_memory()
    content = (
        f"Total Swap: {swap.total / (1024 ** 3):.2f} GB\n"
        f"Used Swap: {swap.used / (1024 ** 3):.2f} GB\n"
        f"Free Swap: {swap.free / (1024 ** 3):.2f} GB\n"
        f"Swap Usage: {swap.percent}%"
    )
    log_html("Swap Usage", content)

def get_disk_io():
    io = psutil.disk_io_counters()
    content = (
        f"Total Read: {io.read_bytes / (1024 ** 3):.2f} GB\n"
        f"Total Write: {io.write_bytes / (1024 ** 3):.2f} GB\n"
        f"Read Count: {io.read_count}\n"
        f"Write Count: {io.write_count}"
    )
    log_html("Disk I/O", content)

def test_disk_speed(file_name="testfile.tmp", size_mb=100):
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
    content = (
        f"Write Speed: {size_mb / write_duration:.2f} MB/s\n"
        f"Read Speed: {size_mb / read_duration:.2f} MB/s"
    )
    log_html("Disk Speed Test", content)

def get_boot_time():
    content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
    log_html("Boot Time", content)

def save_html_report():
    pc_name = socket.gethostname()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pc{pc_name}{timestamp}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("<html><head><title>System Report</title></head><body>")
        f.write(f"<h1>System Report for {pc_name}</h1><p>Generated on: {datetime.now()}</p>")
        f.writelines(html_output)
        f.write("</body></html>")
    print(f"✅ Report saved to: {filename}")

def main():
    get_cpu_spec()
    get_ram_spec()
    get_gpu_spec()
    get_os_spec()
    get_cpu_usage()
    get_ram_usage()
    get_swap_usage()
    get_disk_io()
    test_disk_speed()
    get_boot_time()
    save_html_report()

if __name__ == "__main__":
    main()
