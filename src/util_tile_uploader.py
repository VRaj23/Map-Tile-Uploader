import sys
import os
import untangle
from zoom_level import ZoomLevel
from kml_info import KmlInfo

def end_program():
    print('END')
    sys.exit()

def get_DOC_KML():
    return "doc.kml";

def get_path_with_ending_slash(path):
    if path[-1] == '/':
        return path
    else:
        return path+'/'


def get_path_from_arg(arg):
    if len(arg) != 2:
        print('Incorrect number of arguments')
        end_program()
    else:
        return get_path_with_ending_slash(arg[1])

def read_file_content(path):
    f = open(path, "r")
    return f.read()

def check_doc_kml(list_of_files):
    found = False
    for file_name in list_of_files:
        if file_name == get_DOC_KML():
            found = True
    if found == False:
        print(get_DOC_KML()+' not found in tile directory')
        end_program()

def validate_tile_directory_path(path):
    try:
        current_path = next(os.walk(path))
    except StopIteration:
        print('Invalid Path')
        end_program
    else:
        list_of_files = current_path[2]
        check_doc_kml(list_of_files)

def get_zoom_level_list(tile_directory):
    tile_map_resource = read_file_content(tile_directory+'tilemapresource.xml')
    parsed_kml = untangle.parse(tile_map_resource)
    zoom_level_counter = 0
    zoom_level_list = []
    for item in parsed_kml.TileMap.TileSets.children:
        current_zoom_level = ZoomLevel(zoom_level_counter,item['href'])
        zoom_level_list.append(current_zoom_level)
        zoom_level_counter = zoom_level_counter + 1
    return zoom_level_list

def get_kml_file(obj):
    file_list = obj[2]
    for file in file_list:
        if file[-4:] == '.kml':
            print(get_path_with_ending_slash(obj[0])+file)

def get_file_zoom_level(file):
    print(file)
    return 0

def get_kml_info(obj, zoom_level_list):
    file_list = obj[2]
    for file in file_list:
        if file[-4:] == '.kml' and file[-7:] != 'doc.kml':
            zl = get_file_zoom_level(file)

def get_zoom_directory_root(tile_directory,path):
    sub_directory_path = path[len(tile_directory):]
    return sub_directory_path[:sub_directory_path.find('/')]

def get_zoom_value(zoom_directory_root, zoom_level_list):
    for zoom_level in zoom_level_list:
        if zoom_level.getDirectoryName() == zoom_directory_root:
            return zoom_level.getZoomLevel()
    return None

def add_each_file_to_kml_file_tree(tile_directory, root_path, file_list, zoom_level_list):
    kml_file_list = []
    zoom_directory_root = get_zoom_directory_root(tile_directory,root_path)
    if zoom_directory_root == '':
        return None

    zoom_value = get_zoom_value(zoom_directory_root, zoom_level_list)
    if zoom_value is None:
        return None

    for kml_file in file_list:
        if kml_file[-4:] == '.kml':
            kml_info = KmlInfo(root_path+'/'+kml_file, zoom_value)
            kml_file_list.append(kml_info)
    return kml_file_list


def get_kml_file_tree(tile_directory, zoom_level_list):
    kml_file_tree = []
    for item in os.walk(tile_directory):
        if len(item[2]) == 0:
            continue
        else:
            kml_file_list = add_each_file_to_kml_file_tree(tile_directory,item[0],item[2], zoom_level_list)
            if kml_file_list is None:
                continue
            else:
                for kml_file in kml_file_list:
                    kml_file_tree.append(kml_file)
    return kml_file_tree
