import os
import csv
import base64
import re
from io import StringIO
from config.settings import MEDIA_ROOT
from typing import List, Tuple, Dict
from user.lib import find_admin, create_bulk_user_info, get_list_user_info

def output(message="", data = dict(), errors=list()) -> dict:
    return {
        'message': message,
        'data': data,
        'errors': errors
    }

def authentication(email, password):
    status, user = find_admin(email)
    if status:
        #find user, and check password
        if user.validate_password(password):
            return True, user
    # not Found User or Password is incorrect
    return False, None


def create_csv_file(data_list: list[dict]) -> None:

    # Define the directory where CSV files will be stored
    directory = os.path.join(MEDIA_ROOT)
    
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    name_file = "exported_data.csv"
    csv_file_path = os.path.join(MEDIA_ROOT, name_file)
    
    # Write data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = data_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)
    return name_file


def read_csv_file(csv_base64_content: str):
    try:
        decoded_csv_content = base64.b64decode(csv_base64_content).decode('utf-8')
        csv_file_like_object = StringIO(decoded_csv_content)
        reader = csv.DictReader(csv_file_like_object)
        list_of_dicts = list(reader)
        return True, list_of_dicts
    except:
        return False, None
    
def is_email_valid(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_iran_code(national_id: str) -> bool:
    
    if not re.search(r'^\d{10}$', national_id): 
        return False
    check = int(national_id[9])
    s = sum(int(national_id[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11

def convert_error_to_str(errors: list[dict]) -> str:
    error_str = ''
    for field, field_errors in errors.items():
        error_str += f"{field}: {', '.join(field_errors)}\n"
    return error_str


def response_download_csv(response, file_name):
    csv_file_path = os.path.join(MEDIA_ROOT, file_name)
    with open(csv_file_path, 'r') as csv_file:
        response.write(csv_file.read())
    
    return response


def insert_user_info(data_list: list[Dict[str, str]]) -> Tuple[int, int, List[Dict[str, str]]]:
    success, failed, list_failed = create_bulk_user_info(data_list)
    return success, failed, list_failed

def list_user_info():
    return list(get_list_user_info())