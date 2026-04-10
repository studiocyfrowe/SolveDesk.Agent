from pandas import DataFrame
import pandas as pd
import wmi
import time
from typing import Callable, Dict, Any, List

class WmiLoader:
    def __init__(self, hostname: str):
        self.data_source = wmi.WMI(f'{hostname}')

    def read_data(self,
        max_count: int,
        interval: int,
        collector: Callable[[wmi.WMI], List[Dict[str, Any]]]) -> DataFrame:
        
        history = []
        i = 0
        while i <= max_count:
            data = collector(self.data_source)
            history.extend(data)
            time.sleep(interval)

        df = pd.DataFrame(history)
        return df

