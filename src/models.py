from enums import ProcessingStatus

class ZoomLevel:
    zoom_level = 0
    directory = ""

    def __init__(self, zoom_level, directory):
        self.zoom_level = zoom_level
        self.directory = directory

    def getDirectoryName(self):
        return self.directory

    def getZoomLevel(self):
        return self.zoom_level

    def __str__(self):
        return str(self.getZoomLevel())+" "+self.getDirectoryName()

    __repr__ = __str__

class KmlInfo:
    kml_file_path = ""
    zoom_level_value = 0
    processing_status = ProcessingStatus.UNPROCESSED
    database_id = 0
    parent_database_id = 0

    def __init__(self, kml_file_path, zoom_level_value):
        self.kml_file_path = kml_file_path
        self.zoom_level_value = zoom_level_value

    def __str__(self):
        return self.kml_file_path+", "+str(self.zoom_level_value)+", "+str(self.processing_status)+", "+str(self.database_id)+", "+str(self.parent_database_id)

    __repr__ = __str__


class ParameterList(object):
    index = 0
    id = 0
    name = ''

    def __init__(self, index, id, name):
        self.index = index
        self.id = id
        self.name = name

    def __repr__(self):
        return str(self.index)+" -> "+self.name;

class Parameters(object):
    map_type = None
    district = None
    year = None
    season = None
    crop = None

    def __init__(self, map_type, district):
        self.map_type = map_type
        self.district = district

    def set_year(self, year):
        self.year = year

    def set_season(self, season):
        self.season = season

    def set_crop(self, crop):
        self.crop = crop

    def __repr__(self):
        value = self.map_type
        value += "\ndistrict_id="+str(self.district.id)+", district_name="+self.district.name
        if self.year != None:
            value += "\nyear="+str(self.year)
        if self.season != None:
            value += "\nseason_id="+str(self.season.id)+", season_name="+self.season.name
        if self.crop != None:
            value += "\ncrop_id="+str(self.crop.id)+", crop_name="+self.crop.name
        return value
