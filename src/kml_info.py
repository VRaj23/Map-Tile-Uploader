from zoom_level import ZoomLevel
from processing_status import ProcessingStatus

class KmlInfo:
    kml_file_path = ""
    zoom_level_value = 0
    processed = ProcessingStatus.UNPROCESSED
    database_id = 0
    parent_database_id = 0

    def __init__(self, kml_file_path, zoom_level_value):
        self.kml_file_path = kml_file_path
        self.zoom_level_value = zoom_level_value

    def __str__(self):
        return self.kml_file_path+", "+str(self.zoom_level_value)+", "+str(self.processed)+", "+str(self.database_id)+", "+str(self.parent_database_id)

    __repr__ = __str__
