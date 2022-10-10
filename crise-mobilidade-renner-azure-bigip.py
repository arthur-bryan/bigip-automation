from bigip import BigIpClient
from colorama import Fore, Style
from datetime import datetime
import urllib3
import json
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BIGIP_URL_HOST = "rt-bigip-01"
DEFAULT_PARTITION = "producao"

bigip_client = BigIpClient(BIGIP_URL_HOST)

pools = [
    {
        "pool_name": "pool_ws_mobilidadews_renner_25796",
        "pool_members_port": "25796",
        "pool_members": ["10.51.136.134", "10.51.136.135", "10.51.136.136",
                         "10.51.136.137", "10.51.136.140", "10.51.136.141",
                         "10.51.136.142", "10.51.136.143", "10.51.136.144",
                         "10.51.136.145", "10.51.136.146", "10.51.136.147"]
    }
]

def show_request_response(response):
    status_code = response.status_code
    if 199 < status_code < 400:
        print(f"{Fore.GREEN}Returned code {status_code}: Success{Style.RESET_ALL}")
    elif status_code >= 400:
        message = json.loads(response.text)["message"]
        if "already exists" in message and status_code == 409:
            print(f"{Fore.YELLOW}Returned code {status_code}: {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Returned code {status_code}: {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Returned code {status_code}: {Style.RESET_ALL}")


def add_to_pools(pools_dict):
    for pool in pools_dict:
        for member in pool["pool_members"]:
            response = bigip_client.add_pool_member(DEFAULT_PARTITION, pool["pool_name"], member, pool["pool_members_port"])
            show_request_response(response)


def remove_from_pools(pools_dict):
    for pool in pools_dict:
        for member in pool["pool_members"]:
            response = bigip_client.remove_pool_member(DEFAULT_PARTITION, pool["pool_name"], member, pool["pool_members_port"])
            show_request_response(response)


def main():
    menu_choice = input("""
    \r[ Rollback Renner AWS servers from BigIP pools  ]
    \r[ 1 ] Add members to pools
    \r[ 2 ] Remove members from pools
    \r[ 0 ] Exit
    \r>> """)
    if menu_choice == "1":
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Fore.LIGHTWHITE_EX}[ STARTED AT {current_time} ]{Style.RESET_ALL}")
        add_to_pools(pools)
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Fore.LIGHTWHITE_EX}[ FINISHED AT {current_time} ]{Style.RESET_ALL}")
    elif menu_choice == "2":
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Fore.LIGHTWHITE_EX}[ STARTED AT {current_time} ]{Style.RESET_ALL}")
        remove_from_pools(pools)
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Fore.LIGHTWHITE_EX}[ FINISHED AT {current_time} ]{Style.RESET_ALL}")
    elif menu_choice == "0":
        sys.exit(0)
    else:
        main()


if __name__ == "__main__":
    main()
