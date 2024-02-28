from datetime import datetime
import unittest
import requests_mock

from warsaw_bus_api import ZtmSession
from warsaw_bus_api.models import (
    Location,
    Bus,
)

class TestZtmSchedule(unittest.TestCase):
    def test_get_buses_location(self) -> None:
        ztm = ZtmSession("test")
        url = "http://test.com/"
        ztm.location_endpoint = url
        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                url,
                json={
                    "result": [
                        {
                            "Lines": "130",
                            "Lon": 21.084736,
                            "VehicleNumber": "1000",
                            "Time": "2021-12-20 16:47:03",
                            "Lat": 52.1675208,
                            "Brigade": "1",
                        },
                        {
                            "Lines": "305",
                            "Lon": 21.1429426,
                            "VehicleNumber": "1001",
                            "Time": "2021-12-20 16:47:01",
                            "Lat": 52.1986071,
                            "Brigade": "1",
                        },
                        {
                            "Lines": "213",
                            "Lon": 21.1560425,
                            "VehicleNumber": "1002",
                            "Time": "2021-12-20 16:47:07",
                            "Lat": 52.2140021,
                            "Brigade": "1",
                        },
                    ]
                },
            )
            expected_result = [
                Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 12, 20, 16, 47, 3),
                    "1",
                ),
                Bus(
                    Location(21.1429426, 52.1986071),
                    "305",
                    "1001",
                    datetime(2021, 12, 20, 16, 47, 1),
                    "1",
                ),
                Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 47, 7),
                    "1",
                ),
            ]
            result = ztm.get_buses_location()
            result = ztm.parse_multiple_bus_location_data(result)
            self.assertEqual(result, expected_result)
