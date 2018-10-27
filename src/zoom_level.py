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
