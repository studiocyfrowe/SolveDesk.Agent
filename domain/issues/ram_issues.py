from enum import StrEnum

class RamIssuesEnum(StrEnum):
    SMALL_INCREASE = 'There was a small increase in memory usage'
    MEDIUM_INCREASE = 'There was a medium increase in memory usage'
    HIGH_INCREASE = 'There was a high increase in memory usage'
    HIGH_USAGE = 'Memory usage is consistently high'
    MEMORY_PRESSURE = 'System is under memory pressure'
    POSSIBLE_MEMORY_LEAK = 'Possible memory leak detected (steadily increasing usage)'
    LOW_AVAILABLE_MEMORY = 'Low available memory detected'