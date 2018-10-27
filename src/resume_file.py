import os

RESUME_FILE_NAME = "resume.upload"

def get_content(kml_info_list):
    content = ""
    for entry in kml_info_list:
        content = content + str(entry) + "\n"
    return content

def write_resume_file(tile_directory, kml_info_list):
    print("updating resume file")
    resume_file = open(tile_directory+"resume.upload","w")
    resume_file.write(tile_directory+"\n")
    resume_file.write(get_content(kml_info_list))
    resume_file.close()

def check_resume_file(tile_directory):
    content = next(os.walk(tile_directory))
    file_list = content[2]
    for file_name in file_list:
        if file_name == RESUME_FILE_NAME:
            print('Resume Upload file found\n')
            return True
    return False
