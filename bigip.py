import requests
import json
import os

class BigIpClientError(Exception):
    pass


class BigIpClient:

    def __init__(self, url_host, protocol="https", mgmt_api_path="mgmt/tm/ltm"):
        self.__url_host = url_host
        self.__protocol = protocol
        try:
            self.__username = os.environ["BIGIP_USER"]
            self.__password = os.environ["BIGIP_PASS"]
        except KeyError:
            raise BigIpClientError("Please, set login environment variables!")
        self.__mgmt_api_path = mgmt_api_path

    def get_all_virtual_servers(self, object_type="virtual"):
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}",
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_virtual_server(self, partition, name, object_type="virtual"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{name}"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_virtual_server_stats(self, partition, name, object_type="virtual"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{name}/stats"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_virtual_server_persistence_profiles(self, partition, name, object_type="virtual"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{name}/profiles"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def enable_virtual_server(self, partition, vs_name, object_type):
        headers = {}
        json_data = {
            'enabled': True,
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{vs_name}"
        response = requests.patch(full_url,
                                  headers=headers,
                                  json=json_data,
                                  verify=False,
                                  auth=(self.__username, self.__password))
        return response

    def disable_virtual_server(self, partition, vs_name, object_type):
        headers = {}
        json_data = {
            'disabled': True,
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{vs_name}"
        response = requests.patch(full_url,
                                  headers=headers,
                                  json=json_data,
                                  verify=False,
                                  auth=(self.__username, self.__password))
        return response

    def delete_virtual_server(self, partition, vs_name, object_type="virtual"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{vs_name}"
        response = requests.delete(full_url,
                                   headers=headers,
                                   verify=False,
                                   auth=(self.__username, self.__password))
        return response

    @staticmethod
    def handle_json_virtual_server(json_object):
        pool = json_object["pool"] if "pool" in json_object.keys() else None
        status = "enabled" if "enabled" in json_object.keys() else "disabled" if "disabled" in json_object.keys() else None
        destination = json_object["destination"].split("/")[2::][0]
        virtual_server = {
            "name": json_object["name"],
            "partition": json_object["partition"],
            "address_status": json_object["addressStatus"],
            "destination": destination,
            "status": status,
            "source": json_object["source"],
            "ip_protocol": json_object["ipProtocol"],
            "source_port": json_object["sourcePort"],
            "pool": pool,
            "source_address_translation": json_object["sourceAddressTranslation"]
        }
        return virtual_server

    def get_all_pools(self, object_type="pool"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_pool_stats(self, partition, pool_name, object_type="pool"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{pool_name}/stats"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_pool_members(self, partition, pool_name, object_type="pool"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{pool_name}/members"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def get_pool_member_stats(self, partition, pool_name, member_name, object_type="pool"):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/{object_type}/~{partition}~{pool_name}/members/~{partition}~{member_name}/stats"
        response = requests.get(full_url,
                                headers=headers,
                                verify=False,
                                auth=(self.__username, self.__password))
        return response

    def create_node(self, partition, node_name, ip_address):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/node/"

        data = {"name": node_name, "partition": partition, "address": ip_address}

        response = requests.post(full_url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False,
                                 auth=(self.__username, self.__password))
        return response

    def add_pool_member(self, partition, pool_name, member_name, member_port):
        headers = {
            "Content-Type": "application/json"
        }

        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/pool/~{partition}~{pool_name}/members/"
        data = {"name": f"/{partition}/{member_name}:{member_port}"}
        print(f"Adding {member_name}:{member_port} to {partition}/{pool_name}...")
        response = requests.post(full_url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False,
                                 auth=(self.__username, self.__password))
        return response

    def remove_pool_member(self, partition, pool_name, member_name, member_port):
        full_url = f"{self.__protocol}://{self.__url_host}/{self.__mgmt_api_path}/pool/~{partition}~{pool_name}/members/{member_name}:{member_port}"
        # if self.confirm_delete_from_pool(partition, f"{member_name}:{member_port}", pool_name):
        print(f"Removing {member_name}:{member_port} from {partition}/{pool_name}...")
        response = requests.delete(full_url,
                                   verify=False,
                                   auth=(self.__username, self.__password))
        return response

    def confirm_delete_from_pool(self, partition, target, pool_name):
        try:
            answer = input(f"Do you really want to remove '{target}' from {partition}/{pool_name}? This can't be undone (y/n): ")
        except ValueError:
            print("Invalid input!")
            self.confirm_delete_from_pool(target)
        else:
            return answer in ("S", "s", "Sim", "sim", "Y", "y", "Yes", "yes")


