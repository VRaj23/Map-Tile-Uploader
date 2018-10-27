import requests
import getpass
import util_tile_uploader as util

def get_api_base_url():
    return "http://ec2-13-127-200-147.ap-south-1.compute.amazonaws.com:8222";
    #return "http://localhost:8222";

def test_api_connection():
    print("Checking connection to server...")
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
            login()
        else:
            print("Connection Error in API response")
            print(response.json())
            util.end_program()

def get_crops(access_token):
    return None
