# Python wrapper for the Warsaw data API

This package allow to fetch bus data from API provided by "UM Warszawa" - https://api.um.warszawa.pl/

## Current features

- Fetch ZTM buses real-time location
- Store ZTM buses real-time location over time
- Fetch ZMT bus routes
## Getting Started

## Installation

```
pip install /path/to/package
```

## Using ZtmSession class

### Get buses locations:

We can fetch all location data for buses:

```python
from warsaw_bus_api import ZtmSession

ztm = ZtmSession(apikey='your_api_key') # you can get API KEY on the https://api.um.warszawa.pl/ after you register
buses = ztm.get_buses_location()

for bus in buses:
    print(bus)
```

We can collect and store the data over some time period. Each files name will be a timestamp of the api call 

```python
from warsaw_bus_api import ZtmSession

ztm = ZtmSession(apikey='your_api_key')
ztm.get_buses_location_over_time(60, parent_dir, "/path/to/desired/destination")
```

We can load stored data from a directory:
```python
from warsaw_bus_api import ZtmSession

ztm = ZtmSession(apikey='your_api_key')
buses = ztm.load_buses_locations("/path/to/desired/destination")

for buses in location:
    for bus in buses:
        print(bus)
```
