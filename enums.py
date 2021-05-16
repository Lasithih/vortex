from enum import Enum

class Env(Enum):
    Production = 1
    Development = 2

class JobType(Enum):
    Youtube = 1
    Direct = 2