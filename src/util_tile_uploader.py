import sys
import os

import untangle

from models import ZoomLevel, KmlInfo, ParameterList, Parameters
from enums import MapType
import api_util as api


def banner():
    print("")
    print("")
    print("***************************")
    print("Launching Map Tile Uploader")
    print("Version: 1")
    print("***************************")
    print("")
    print("")

def end_program():
    print("END")
    sys.exit()

def get_doc_kml():
    return "doc.kml";

def get_tilemapresource():
    return "tilemapresource.xml";

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

def check_files(list_of_files):
    found_doc_kml = False
    found_tilemapresource = False
    for file_name in list_of_files:
        if file_name == get_doc_kml():
            found_doc_kml = True
        if file_name == get_tilemapresource():
            found_tilemapresource = True
    if found_doc_kml == False:
        print(get_doc_kml()+" not found in given Map Tile folder \n")
    if found_tilemapresource == False:
        print(get_tilemapresource()+" not found in given Map Tile folder \n")
    return found_doc_kml and found_tilemapresource

def validate_tile_directory_path(path):
    try:
        current_path = next(os.walk(path))
    except StopIteration:
        print("Invalid Path")
        return None
    else:
        list_of_files = current_path[2]
        if check_files(list_of_files):
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
    if year >= 1970 and year < 2030:
        print('')
        return year
    else:
        print("Invalid Year value \n")
        return get_year()

def print_list(input_list):
    for item in input_list:
        print(item)

def get_selected_item_from_list(indexed_list, parameter_name):
    selection = input("Select "+parameter_name+" Number : ")
    selection = int(selection)#TODO should be number
    if selection < 1 or selection > len(indexed_list):
        print("Invalid Selection \n")
        return get_selected_item_from_list(indexed_list, parameter_name)
    else:
        for item in indexed_list:
            if item.index == selection:
                print("\n\t"+item.name+" Selected\n\n")
                return item
        return None #raise exception

def get_indexed_list(response, id_key, name_key):
    indexed_list = []
    index =  1
    for obj in response:
        indexed_list.append( ParameterList(index, int(obj[id_key]), obj[name_key].capitalize()) )
        index = index + 1
    return indexed_list

def get_parameter(function, access_token, query_param, id_key, name_key, parameter_name):
    response = function(access_token, query_param)
    indexed_list = get_indexed_list(response, id_key, name_key)
    print_list(indexed_list)
    return get_selected_item_from_list(indexed_list, parameter_name)

def get_map_type(): #TODO refactor
    indexed_list = []
    index = 1
    for map in MapType:
        indexed_list.append( ParameterList(index, index, map.name) )
        index = index + 1
    print_list(indexed_list)
    selection = input("Select Map Type Number : ")
    selection = int(selection)#TODO should be number
    if selection < 1 or selection > len(indexed_list):
        print("Invalid Selection \n")
        return get_map_type(indexed_list)
    else:
        for item in indexed_list:
            if item.index == selection:
                print("\t"+item.name+" Selected\n")
                return item.name

def update_parameters_by_map_type(map_type, parameters, access_token, country_id):
    if map_type == 'CropMap' or map_type == 'YieldMap':
        year = get_year()
        parameters.set_year(year)
        season = get_parameter(api.get_seasons,access_token,country_id,"cropSeasonID","cropSeasonName","Season")
        parameters.set_season(season)
        crop = get_parameter(api.get_crops, access_token,None, "cropTypeID", "cropTypeName", "Crop")
        parameters.set_crop(crop)
    elif map_type == 'NDVI' or map_type == 'IDSI':
        year = get_year()
        parameters.set_year(year)
        season = get_parameter(api.get_seasons,access_token,country_id,"cropSeasonID","cropSeasonName","Season")
        parameters.set_season(season)
    return parameters

def confirm_parameter_selection(parameters):
    print("\nConfirm Selection:\n")
    print("\n\tMap Type = "+parameters.map_type)
    print("\n\tDistrict = "+parameters.district.name)
    if parameters.year != None:
        print("\n\tYear = "+str(parameters.year))
    if parameters.season != None:
        print("\n\tSeason = "+str(parameters.season.name))
    if parameters.crop != None:
        print("\n\tCrop = "+str(parameters.crop.name))
    choice = input("Enter Y or N : ")
    if choice == 'y' or choice == 'Y':
        return True
    elif choice == 'n' or choice == 'N':
        return False
    else:
        print('\nInvalid Input')
        return confirm_parameter_selection(parameters)

def get_parameters(access_token):
    map_type = get_map_type()
    country_param = get_parameter(api.get_countries, access_token,None, "countryID", "countryName", "Country")
    state_param = get_parameter(api.get_states,access_token,str(country_param.id),"stateID","stateName","State")
    district_param = get_parameter(api.get_districts,access_token,str(state_param.id),"districtID","districtName","District")
    parameters = Parameters(map_type, district_param)
    parameters = update_parameters_by_map_type(map_type, parameters, access_token, str(country_param.id))
    if confirm_parameter_selection(parameters):
        return parameters
    else:
        print("\n\nRe-Enter Parameters")
        return get_parameters(access_token)
