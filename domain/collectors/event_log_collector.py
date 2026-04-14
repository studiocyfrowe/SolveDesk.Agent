from domain.abstracts.base_collector import BaseCollector
import wmi, pythoncom, time

class EventLogCollector(BaseCollector):
    def collect_data(self, hostname: str) -> list:
        pythoncom.CoInitialize()

        try:
            conn = wmi.WMI(hostname)

            rows: list = []
            query = """
                SELECT TimeGenerated, SourceName, EventCode, Message
                FROM Win32_NTLogEvent
                WHERE Logfile = 'System'
                AND SourceName = 'Service Control Manager'
                AND (EventCode = '7000' OR EventCode = '7031' OR EventCode = '7034')
            """

            for log in conn.query(query):
                rows.append({
                    "TimeGenerated": log.TimeGenerated,
                    "EventCode": log.EventCode,
                    "Message": log.Message
                })

            return rows

        finally:
            pythoncom.CoUninitialize()