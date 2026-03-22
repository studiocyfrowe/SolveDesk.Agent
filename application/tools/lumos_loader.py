from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

class LumosLoader:
    def __init__(self):
        self.engine = create_engine(os.getenv('CONNECTION_STRING'))

    def fetch_memory_ram_scan(self):
        query = text("""SELECT 
            AVG(TotalGB)     AS AvgTotalGB,
            AVG(UsedGB)      AS AvgUsedGB,
            AVG(FreeGB)      AS AvgFreeGB,
            AVG(UsedPercent) AS AvgUsedPercent
        FROM MemoryRamScans""")

        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()

        return [dict(row._mapping) for row in rows]

    def fetch_processes_scan(self):
        query = text("""SELECT 
            Id, 
            MachineGuid, 
            ProcessId, 
            ProcessName, 
            MemoryUsageMB, 
            CpuUsagePercent, 
            StartTime, 
            LastScan
        FROM Processes
        ORDER BY MemoryUsageMB DESC
        LIMIT 25""")

        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()

        return [dict(row._mapping) for row in rows]