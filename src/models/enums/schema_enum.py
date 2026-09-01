from enum import Enum

class CompanyMappingType(str,Enum):
    STRING="string"
    INTEGER="integer"
    NUMBER="number"
    BOOLEAN="boolean"