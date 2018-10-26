import requests
import util_tile_uploader as util

def get_api_base_url():
    return 'http://ec2-13-127-200-147.ap-south-1.compute.amazonaws.com:8222';

def test_api_connection():
    try:
        response = requests.get(get_api_base_url()+'/')
    except:
        print('Unable to call API. \nPlease check Internet connection')
        util.end_program()
    else:
        if response.status_code == 200:
            print(response.json())
        else:
            print('Error in API response')
            print(response.json())
            util.end_program()
