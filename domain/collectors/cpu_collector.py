from domain.abstracts.base_collector import BaseCollector

class CPUCollector(BaseCollector):
    def __init__(self, data_source):
        self.data_source = data_source

    def collect_data(self) -> []:
        rows = []

        for cpu in self.data_source.Win32_Processor():
            rows.append({
                "Caption": cpu.Caption,
                "Description": cpu.Description,
                "LoadPercentage": cpu.LoadPercentage,
                "MaxClockSpeed": cpu.MaxClockSpeed
            })

        return rows