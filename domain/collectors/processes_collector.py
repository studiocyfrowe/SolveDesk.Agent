from domain.abstracts.base_collector import BaseCollector
import pythoncom
import wmi
import time

class ProcessesCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows: list = []
            i = 0
            
            while i <= 5:
                for p in conn.Win32_Process():
                    rows.append({
                        "ProcessName": p.Name,
                        "ProcessId": p.ProcessId,
                        "ParentProcessId": p.ParentProcessId,
                        "ThreadCount": p.ThreadCount,
                        "HandleCount": p.HandleCount,
                        "WorkingSet_MB": round(int(p.WorkingSetSize) / (1024**2), 2) if p.WorkingSetSize else None,
                        "CreationDate": p.CreationDate
                    })
                i += 1
                time.sleep(5)

            return rows

        finally:
            pythoncom.CoUninitialize()