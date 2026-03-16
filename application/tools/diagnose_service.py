import psutil

class DiagnoseService:
    def check_ram_usage(self):
        ram = psutil.virtual_memory()
        return {
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "ram_used_percent": ram.percent
        }

    def check_cpu_usage(self):
        cpu = psutil.cpu_percent(interval=1)
        return {
            "cpu_usage_percent": cpu
        }

    def check_disk_space(self):
        disk = psutil.disk_usage("/")
        return {
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_used_percent": disk.percent
        }

    def top_processes(self):
        processes = []

        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(p.info)
            except:
                pass

        processes = sorted(
            processes,
            key=lambda x: x['cpu_percent'],
            reverse=True
        )

        return processes[:5]