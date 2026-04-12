from domain.abstracts.base_collector import BaseCollector
import pythoncom
import wmi
import time

class RAMCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows: list = []
            i = 0

            while i <= 5:
                for ram in conn.Win32_OperatingSystem():
                    total = int(ram.TotalVisibleMemorySize)
                    free = int(ram.FreePhysicalMemory)

                    used = total - free
                    used_percent = (used / total) * 100

                    rows.append({
                        "DeviceName": ram.CSName,
                        "Total_MB": round(total / 1024, 2),
                        "Used_MB": round(used / 1024, 2),
                        "Free_MB": round(free / 1024, 2),
                        "Used_Percentage": round(used_percent, 2)
                    })
                    i += 1
                    time.sleep(5)

            return rows

        finally:
            pythoncom.CoUninitialize()