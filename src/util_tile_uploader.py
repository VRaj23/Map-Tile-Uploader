import sys
import os
import untangle
from zoom_level import ZoomLevel
from kml_info import KmlInfo
from parameters import SelectedParameters

def banner():
    print("")
    print("")
    print("***************************")
    print("Launching Map Tile Uploader")
    print("***************************")
    print("")
    print("")

def end_program():
    print("END")
    sys.exit()

def get_DOC_KML():
    return "doc.kml";

def get_path_with_ending_slash(path):
    if path[-1] == "/":
        return path
    else:
        return path+"/"

def read_file_content(path):
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def check_doc_kml(list_of_files): #check tilemapresource.xml
    found = False
    for file_name in list_of_files:
        if file_name == get_DOC_KML():
            found = True
    if found == False:
        print(get_DOC_KML()+" not found in given Map Tile folder \n")
    return found

def validate_tile_directory_path(path):
    try:
        current_path = next(os.walk(path))
    except StopIteration:
        print("Invalid Path")
        return None
    else:
        list_of_files = current_path[2]
        if check_doc_kml(list_of_files):
            return path
        else:
            return None

def get_tile_directory():
    path = input("Enter path for Map Tile folder: ")
    if validate_tile_directory_path(path) == None:
        return get_tile_directory()
    else:
        print("")
        return get_path_with_ending_slash(path)

def get_zoom_level_list(tile_directory):
    tile_map_resource = read_file_content(tile_directory+"tilemapresource.xml")
    parsed_kml = untangle.parse(tile_map_resource)
    zoom_level_counter = 0
    zoom_level_list = []
    for item in parsed_kml.TileMap.TileSets.children:
        current_zoom_level = ZoomLevel(zoom_level_counter,item["href"])
        zoom_level_list.append(current_zoom_level)
        zoom_level_counter = zoom_level_counter + 1
    return zoom_level_list

def get_zoom_directory(tile_directory, path):
    return path[len(tile_directory):]

def get_zoom_directory_root(tile_directory,path):
    sub_directory_path = get_zoom_directory(tile_directory,path)
    return sub_directory_path[:sub_directory_path.find("/")]

def get_zoom_value(zoom_directory_root, zoom_level_list):
    for zoom_level in zoom_level_list:
        if zoom_level.getDirectoryName() == zoom_directory_root:
            return zoom_level.getZoomLevel()
    return None

def add_each_file_to_kml_file_tree(tile_directory, root_path, file_list, zoom_level_list):
    kml_file_list = []
    zoom_directory_root = get_zoom_directory_root(tile_directory,root_path)
    if zoom_directory_root == "":
        return None

    zoom_value = get_zoom_value(zoom_directory_root, zoom_level_list)
    if zoom_value is None:
        return None

    for kml_file in file_list:
        if kml_file[-4:] == ".kml":
            kml_info = KmlInfo(zoom_directory_root+"/"+kml_file, zoom_value)
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

def get_year():
    year = input("Year : ")
    year = int(year)
    if year >= 1970:
        return year
    else:
        print("Invalid Year value \n")
        return get_year()

def get_crop_id():
    return 0

def get_parameters():
    crop_id = get_crop_id()
    year = get_year()
    parameters = SelectedParameters(crop_id, year)
    print(parameters)
    return parameters
