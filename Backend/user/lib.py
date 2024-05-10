from .models import AdminUser
from typing import Optional, Tuple
from .models import UserInfo
from typing import List, Tuple, Dict



def find_admin(email: str) -> Tuple[bool, Optional[AdminUser]]:
    try:
        user = AdminUser.objects.filter(username=email)
        return True, user

    except Exception as ex:
        return False, None


def create_bulk_user_info(data_list: List[Dict[str, str]]) -> Tuple[int, int, List[Dict[str, str]]]:
    not_insert_data = []
    counter_add = 0
    counter_failed = 0
    for item in data_list:
        try:
            UserInfo.objects.create(email=item['email'], national_id=item['national_id'])
            counter_add += 1
        except:
            counter_failed += 1
            not_insert_data.append({
                'email': item['email'],
                'national_id': item['national_id'],
                'message': 'Inserted Before'
            })

    return counter_add, counter_failed, not_insert_data

def get_list_user_info():
    return UserInfo.objects.values('email', 'national_id')