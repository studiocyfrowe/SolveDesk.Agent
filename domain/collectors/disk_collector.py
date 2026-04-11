from domain.abstracts.base_collector import BaseCollector
import pythoncom
import wmi

class DiskCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows = []
            for disk in conn.Win32_LogicalDisk(DriveType=3):
                rows.append({
                    "DeviceID": disk.DeviceID,
                    "Description": disk.Description,
                    "FileSystem": disk.FileSystem,
                    "SystemName": disk.SystemName,
                    "FreeSpace": disk.FreeSpace,
                    "Size": disk.Size
                })

            return rows

        finally:
            pythoncom.CoUninitialize()