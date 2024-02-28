"""Models for the stored api data"""
#pylint: disable=too-many-arguments

from datetime import datetime
from dataclasses import dataclass
@dataclass
class Location:
    """Location model"""
    longitude: float
    latitude: float

    def __init__(self, longitude: float, latitude: float) -> None:
        self.longitude = longitude
        self.latitude = latitude
    
    def __eq__(self, other):
        if not isinstance(other, Location):
            raise NotImplementedError
        return self.__dict__ == other.__dict__


class Bus:
    """Vehicle model"""
    location: Location
    line: str
    bus_id: str
    time: datetime
    brigade: str

    def __init__(
        self,
        location: Location,
        line: str,
        bus_id: str,
        time: datetime,
        brigade: str,
    ) -> None:
        self.location = location
        self.lines = line
        self.bus_id = bus_id
        self.time = time
        self.brigade = brigade

    def __str__(self):
        return (
            f"Bus(line={self.lines}, number={self.bus_id}, "
            f"lat={self.location.latitude}, lon={self.location.longitude}, "
            f"time={self.time})"
        )
    
    def __eq__(self, other):
        if not isinstance(other, Bus):
            raise NotImplementedError
        return self.__str__() == other.__str__()
    