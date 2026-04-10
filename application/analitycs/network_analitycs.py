from pandas import DataFrame
from domain.abstracts.base_analysis_service import BaseAnalysisService
from typing import Optional
import psutil
import pandas as pd

class NetworkAnalitycs(BaseAnalysisService):
    def __init__(self, loader):
        self.loader = loader

    def load_data(self):
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
        io = psutil.net_io_counters(pernic=True)

        networks = []

        for iface in stats:
            if stats[iface].isup:
                iface_addresses = [
                    addr.address for addr in addrs.get(iface, [])
                ]

                sent = io[iface].bytes_sent / (1024 * 1024) if iface in io else 0
                recv = io[iface].bytes_recv / (1024 * 1024) if iface in io else 0

                item = {
                    "interface": iface,
                    "status": stats[iface].isup,
                    "speed_mbps": stats[iface].speed,
                    "sent_mb": round(sent, 2),
                    "recv_mb": round(recv, 2),
                    "addresses": ", ".join(iface_addresses)
                }

                networks.append(item)

        df = pd.DataFrame(networks)
        return df
        
    def analyze(self, df: DataFrame) -> DataFrame:
        grouped = df.groupby('StationName').agg({
            "UsedPercent": ['mean', 'max']
        })

        grouped = grouped.reset_index()
        grouped.columns = ['StationName', 'used_percent_mean', 'used_percent_max']

        return grouped
    
    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:
        issues = []

        if grouped["used_percent_mean"].mean() > 80:
            issues.append("Sustained high CPU usage across processes")

        if grouped["used_percent_max"].max() > 80:
            issues.append("Single process reached very high CPU usage (possible CPU spike)")

        return issues
    
    def build_llm_payload(
        self,
        top_processes: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None,
        issues: Optional[list] = None
    ) -> dict:
        payload = {
            "processor_scan": {
                "processor_used_percent_mean": round(df["used_percent_mean"].mean(), 2),
                "processor_used_percent_max": round(df["used_percent_max"].max(), 2)
            },
            "issues": issues
        }

        return payload