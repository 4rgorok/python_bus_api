"""Implementation of the ZtmSession class"""
# pylint: disable=E1101
from datetime import datetime
import time
import os
import ast
from typing import Dict, Optional, Union
import requests

from .models import Bus, Location

class ZtmSession():
    """ZtmSession class"""
    apikey: str
    location_endpoint: str
    schedule_endpoint: str

    def __init__(self, apikey) -> None:
        self.apikey = apikey
        self.location_endpoint = "https://api.um.warszawa.pl/api/action/busestrams_get"
        self.routes_endpoint = "https://api.um.warszawa.pl/api/action/public_transport_routes"

    def __get_data_from_ztm(
        self, url, query_params: Dict[str, Union[str, int, None]]
    ):
        req = requests.get(url=url, params=query_params, timeout=10)
        if req.status_code == requests.codes.ok:
            res = req.json()
        else:
            raise ConnectionError(f"Error fetching data from {url}, status: {req.status_code}")

        if res.get("error"):
            raise ConnectionError(res["error"])

        return res["result"]

    def __parse_bus_location_data(self, record):
        return Bus(
            location=Location(
                longitude=float(record["Lon"]), latitude=float(record["Lat"])
            ),
            line=record["Lines"],
            bus_id=record["VehicleNumber"],
            time=datetime.strptime(record["Time"], "%Y-%m-%d %H:%M:%S"),
            brigade=record["Brigade"],
        )

    def parse_multiple_bus_location_data(self, records):
        """Parsing result from api call to list of buses"""
        buses = []
        for record in records:
            buses.append(self.__parse_bus_location_data(record=record))
        return buses

    def __get_bus_location(
        self, line: Optional[str] = None
    ):
        query_params: Dict[str, Union[str, int, None]] = {
            "resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59",
            "type": 1,
            "apikey": self.apikey,
            "line": line,
        }
        response = self.__get_data_from_ztm(self.location_endpoint, query_params)
        return response

    def load_buses_locations(self, location):
        """Load all the buses location from directory"""
        locations_list = []
        for file in os.listdir(location):
            file_location = os.path.join(location, os.fsdecode(file))
            with open(file_location, encoding="utf-8") as f:
                data = f.read()
            res = ast.literal_eval(data)
            locations_list.append(self.parse_multiple_bus_location_data(res))
        return locations_list

    def get_buses_location(self, line: Optional[str] = None):
        """Get location of all buses with given line number, returns List of Bus objects"""
        return self.__get_bus_location(line=line)

    def get_buses_location_over_time(self, minutes, destination, folder_name):
        """Collect buses location over time"""
        path = os.path.join(destination, folder_name)
        os.mkdir(path)
        for x in range(minutes):
            current_data = ""
            while len(current_data) < 1000:
                current_data = self.__get_bus_location()
            now = datetime.now()
            file_name = now.strftime("%d-%m-%Y_%H-%M") + ".json"
            with open(os.path.join(path, file_name), 'w', encoding="utf-8") as temp_file:
                print(current_data, file=temp_file)
            print(f"{x + 1}/{minutes} done")
            time.sleep(60)

    def get_bus_routes(self):
        """Get bus routes for all lines"""
        query_params: Dict[str, Union[str, int, None]] = {
            "apikey": self.apikey,
        }
        response = self.__get_data_from_ztm(self.routes_endpoint, query_params)
        return response
