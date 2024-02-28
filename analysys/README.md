# Analisys library for the data from Warsaw public api

## Current features

- Analise and plot the speeding of the buses
- Plot routes for specific buses
- Plot data on an interactive map of Warsaw
- Analise number of active buses at the time
- Analise the correctness of the data
- Analise and plotplaces where buses stop most often
## Getting Started

## Installation

```
pip install /path/to/package
```

## Using the library module

### Prepare the data for further analisys:

We get the ids of the active buses:

```python
from bus_data_analisys import get_active_numbers

active_numbers = get_active_numbers(locations) # `locations` is the list returned by ztm.load_buses_locations("/path/to/desired/destination")

for bus_id in active_numbers:
    print(bus_id)
```

We can extract a singe bus route from the entire list:

```python
from bus_data_analisys import get_single_bus_route

bus_route = get_single_bus_route(locations, "bus_id") # `locations` is the list returned by ztm.load_buses_locations("/path/to/desired/destination")

for bus in bus_route:
    print(bus)
```

We can extract all of the routes of the active buses from the entire list:
```python
from bus_data_analisys import get_active_buses_list

bus_routes = get_active_buses_list(locations)

for bus_route in bus_routes:
    for bus in bus_route:
        print(bus)
```

### Plot recorded bus route:

We can plot a line map of a bus route on an interactive map of Warsaw:

```python
import from bus_data_analisys import *

active_locations = get_active_buses_list(locations)
plot_route(active_locations, "bus_id")
```

### Data analisys:

We can check how many buses exeded the speed limit and plot all of the ocurences on a scatter map on an interactive map of Warsaw:

```python
import from bus_data_analisys import *

active_locations = get_active_buses_list(locations)
number_of_speeding_buses = plot_speeding_buses(active_locations)

print(f"Number of buses that exeded the speed limit: {number_of_speeding_buses}")
```

We can check and plot where the buses stopped moving:

```python
import from bus_data_analisys import *

active_locations = get_active_buses_list(locations)
plot_stopped_places(active_locations)
```

We can check and plot the distribution of velocities of the buses on a given range:

```python
import from bus_data_analisys import *

active_locations = get_active_buses_list(locations)
plot_bus_speeds(active_locations1, "min_value", "max_value")
```

### Looking for data inacuracies

We can see what percentage of the buses are updating their location properly:

```python
import from bus_data_analisys import *

p_of_active = percent_of_buses_active(locations)
print(f"{int(p_of_active)}% of buses are active")
```

We can look for velocity anomalies and check what percentage of data is inacurate (e.g. the data shows a speed of 1000km/h which is phisically impossible, the function conciders any speed above 100km/h to be inacurate):

```python
import from bus_data_analisys import *

p_of_anomalies = percent_of_speed_anomalies(active_locations1)
print(f"{round(p_of_anomalies,2)}% of speed anomalies")
```

### Optimising the use of the functions:

Note that the most time-consuming function is the `load_buses_locations()` from the `warsaw_bus_api` module and the `get_active_buses_list()` as they need to load the data from files and rearange it for further analisys, therefore it's best to use them only once (for each data set) at the begining of the program.