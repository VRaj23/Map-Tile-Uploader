import sys

import util_tile_uploader as util
import api_util as api
from models import ZoomLevel
import resume_file as resume

util.banner()
api.test_api_connection()
access_token = api.login()
tile_directory = util.get_tile_directory()
resume_file = resume.check_resume_file(tile_directory)
#resume or start new (y/n) ?

selected_parameters = util.get_parameters(access_token)
#confirm selection

#zoom levels
zoom_level_list = util.get_zoom_level_list(tile_directory)
print(zoom_level_list)

#prepare kml file tree
kml_file_tree = util.get_kml_file_tree(tile_directory, zoom_level_list)

for item in kml_file_tree:
    print(item)

print(len(kml_file_tree))
resume.write_resume_file(tile_directory,kml_file_tree,selected_parameters)
