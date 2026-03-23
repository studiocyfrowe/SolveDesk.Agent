class StatisticsController:
    def __init__(self, loader):
        self.loader = loader

    def get_cpu_data(self):
        return self.loader.fetch_cpu_scan()