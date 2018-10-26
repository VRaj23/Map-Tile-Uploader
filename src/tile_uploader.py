import sys
import util_tile_uploader as util
import api_util as api
from zoom_level import ZoomLevel

api.test_api_connection()

#login

#get directory path
tile_directory = util.get_path_from_arg(sys.argv)
util.validate_tile_directory_path(tile_directory)

#check for resume file

#if resume file not found then get metadata-> map type, state, year, season
'''
kml = util.read_file_content(tile_directory+util.get_DOC_KML())
print(kml)
obj = untangle.parse(kml)
print(obj.kml.Document.NetworkLink.Region.LatLonAltBox.north.cdata)
'''

#zoom levels
zoom_level_list = util.get_zoom_level_list(tile_directory)
print(zoom_level_list)

#prepare kml file tree
kml_file_tree = util.get_kml_file_tree(tile_directory, zoom_level_list)

for item in kml_file_tree:
    print(item)

print(len(kml_file_tree))
