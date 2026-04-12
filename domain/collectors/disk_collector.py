from domain.abstracts.base_collector import BaseCollector
import pythoncom
import wmi
import time

class DiskCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows: list = []
            i = 0
            
            while i <= 5:
                for disk in conn.Win32_LogicalDisk(DriveType=3):
                    rows.append({
                        "DeviceID": disk.DeviceID,
                        "Description": disk.Description,
                        "FileSystem": disk.FileSystem,
                        "SystemName": disk.SystemName,
                        "FreeSpace": disk.FreeSpace,
                        "Size": disk.Size
                    })
                i += 1
                time.sleep(5)

            return rows

        finally:
            pythoncom.CoUninitialize()