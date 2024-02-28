from datetime import datetime
import unittest

from bus_data_analisys import (
    calculate_distance,
    calculate_velocity
)
from warsaw_bus_api.ztm.models import (
    Location,
    Bus,
)

class TestDistance(unittest.TestCase):
    def test_calculate_distance(self) -> None:
        reading1 = Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 12, 20, 16, 47, 3),
                    "1",
                )
        reading2 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        result = calculate_distance(reading1, reading2)
        expected_result = 7.108341787831862
        self.assertEqual(result, expected_result)


class TestVelocity(unittest.TestCase):
    def test_calculate_velocity(self) -> None:
        reading1 = Bus(
                    Location(21.084736, 52.1675208),
                    "130",
                    "1000",
                    datetime(2021, 12, 20, 16, 47, 3),
                    "1",
                )
        reading2 = Bus(
                    Location(21.1560425, 52.2140021),
                    "213",
                    "1002",
                    datetime(2021, 12, 20, 16, 48, 7),
                    "1",
                )
        result = calculate_velocity(reading1, reading2)
        expected_result = 399.8442255655423
        self.assertEqual(result, expected_result)
