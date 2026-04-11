from domain.abstracts.base_collector import BaseCollector
import pythoncom
import wmi

class CPUCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows = []
            for cpu in conn.Win32_Processor():
                rows.append({
                    "Caption": cpu.Caption,
                    "Description": cpu.Description,
                    "LoadPercentage": cpu.LoadPercentage,
                    "MaxClockSpeed": cpu.MaxClockSpeed
                })

            return rows

        finally:
            pythoncom.CoUninitialize()