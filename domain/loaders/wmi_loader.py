from domain.abstracts.base_collector import BaseCollector
import pythoncom
from pandas import DataFrame
import time
import wmi
import pandas as pd

class WmiLoader:
    def read_data(self, max_count, interval, collector) -> DataFrame:
        history = []

        for _ in range(max_count):
            data = collector.collect_data()

            if data:
                history.extend(data)

            time.sleep(interval)

        return pd.DataFrame(history)