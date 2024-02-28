from datetime import datetime
import unittest

from bus_data_analisys import (
    get_active_numbers,
    percent_of_buses_active,
    percent_of_speed_anomalies,
)
from warsaw_bus_api.ztm.models import (
    Location,
    Bus,
)


class TestActive(unittest.TestCase):
    def test_count_active(self) -> None:
        reading1 = Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 10, 20, 16, 48, 3),
                    "1",
                )
        reading2 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        reading3 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        result = get_active_numbers([[reading1, reading2, reading3]])
        expected_result = 2
        self.assertEqual(len(result), expected_result)

    def test_percent_active(self) -> None:
        reading1 = Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 12, 20, 16, 46, 3),
                    "1",
                )
        reading2 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        reading3 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        reading4 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 10, 20, 16, 48, 7),
                    "1",
                )
        result = percent_of_buses_active([[reading1, reading2, reading3, reading4]])
        expected_result = 50
        
        self.assertEqual(result, expected_result)

class TestAnomalies(unittest.TestCase):
    def test_percent_anomalies(self) -> None:
        reading1 = Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 12, 20, 16, 46, 3),
                    "1",
                )
        reading2 = Bus(
                    Location(21.1560425, 53.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        reading3 = Bus(
                    Location(21.1560425, 53.2240021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 49, 7),
                    "1",
                )
        result = percent_of_speed_anomalies([[reading1, reading2, reading3]])
        expected_result = 50
        self.assertEqual(result, expected_result)    