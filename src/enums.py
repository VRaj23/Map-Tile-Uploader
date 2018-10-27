from enum import Enum

class ProcessingStatus(Enum):
    UNPROCESSED = 0
    PARTIAL = 1
    PROCESSED = 2

class MapType(Enum):
    CropMap = "Crop Map"
    YieldMap = "Yield Map"
    NDVI = "NDVI Map"
    FloodReoccurance = "Flood Reoccurance Map"
    IDSI = "IDSI Map"
