import wmi

def check_system_health():

    w = wmi.WMI()

    cpu = w.Win32_Processor()[0].LoadPercentage

    os = w.Win32_OperatingSystem()[0]

    total = int(os.TotalVisibleMemorySize)
    free = int(os.FreePhysicalMemory)

    ram = (total - free) / total * 100

    disks = []

    for disk in w.Win32_LogicalDisk(DriveType=3):
        size = int(disk.Size)
        free = int(disk.FreeSpace)
        used = (size - free) / size * 100
        disks.append(f"{disk.DeviceID}: {used:.1f}%")

    return {
        "cpu_usage": cpu,
        "ram_usage": round(ram,2),
        "disks": disks
    }

print(check_system_health())