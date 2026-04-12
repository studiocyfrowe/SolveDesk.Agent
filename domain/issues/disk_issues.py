from enum import StrEnum

class DiskIssuesEnum(StrEnum):
    SMALL_INCREASE = 'There was a small increase in disk involvement'
    MEDIUM_INCREASE = 'There was a medium increase in disk involvement'
    HIGH_INCREASE = 'There was a high increase in disk involvement'