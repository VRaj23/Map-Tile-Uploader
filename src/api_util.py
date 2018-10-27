import requests
import getpass

import util_tile_uploader as util

def get_api_base_url():
    return "http://ec2-13-127-200-147.ap-south-1.compute.amazonaws.com:8222";
    #return "http://localhost:8222";

def test_api_connection():
    print("Checking connection to server "+get_api_base_url())
    try:
        response = requests.get(get_api_base_url()+"/")
    except:
        print("Connection Error: Unable to call API. \nPlease check Internet connection")
        util.end_program()
    else:
        if response.status_code == 200:
            print("Connection OK")
        else:
            print("Connection Error in API response")
            print(response.json())
            util.end_program()

def check_user_role(role):
    if role != "ROLE_ANALYST":
        print("Not an Analyst User")
        util.end_program()

def login():
    print("")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    print("")
    try:
        response = requests.post(get_api_base_url()+"/login", json = {"email":email, "password":password})
    except:
        print("Connection Error")
        test_api_connection()
    else:
        if response.status_code == 200:
            check_user_role(response.json()["message"])
            print("Login Successful \n")
            return response.json()["response"]["value"]
        elif response.status_code == 401:
            print("Incorrect email/password")
            return login()
        else:
            print("Connection Error in API response")
            print(response.json())
            util.end_program()

def get_header(access_token):
    return {"Authorization": access_token}

def get_response(access_token, api_sub_path):
    try:
        response = requests.get(get_api_base_url()+api_sub_path, headers=get_header(access_token))
    except:
        print("Connection Error")
        test_api_connection()
    else:
        return response.json()["response"]

def get_countries(access_token, query_param):
    print('Fetching list of countries from server...')
    return get_response(access_token, "/auth/analyst/v1/country/all")

def get_states(access_token, query_param):
    print('Fetching list of states from server...')
    return get_response(access_token,"/auth/analyst/v1/states?countryID="+query_param)

def get_districts(access_token, query_param):
    print('Fetching list of districts from server...')
    return get_response(access_token,"/auth/analyst/v1/districts?stateID="+query_param)

def get_seasons(access_token, query_param):
    print('Fetching list of seasons from server...')
    return get_response(access_token,"/auth/analyst/v1/seasons?countryID="+query_param)

def get_crops(access_token, query_param):
    print('Fetching list of crops from server...')
    return get_response(access_token,"/auth/analyst/v1/crops")
