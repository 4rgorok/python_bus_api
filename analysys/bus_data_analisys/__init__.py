"""Bus data analisys functions"""

import geopy.distance
import plotly.express as px

import matplotlib.pyplot as plt
import numpy as np

def get_active_numbers(locations):
    """Get list of id of active buses"""
    biggest = locations[0][0].time
    active_list = []
    # Find the most recent recorded time from this call
    for bus in locations[0]:
        if bus.time > biggest:
            biggest = bus.time
    # Due to inactive busses not updating their time we need to
    # only look at those that updated it
    for bus in locations[0]:
        if (biggest - bus.time).total_seconds() < 60:
            active_list.append(bus.bus_id)

    return active_list

def get_single_bus_route(locations, bus_number):
    """Get recorded route for a specific bus"""
    current_bus = []
    for buses in locations:
        for bus in buses:
            if bus.bus_id == str(bus_number):
                current_bus.append(bus)
    return current_bus

def get_active_buses_list(locations):
    """Get list of recorded active bus routes"""
    active_buses_list = []
    active_buses = get_active_numbers(locations)
    for bus_number in active_buses:
        current_bus = get_single_bus_route(locations, bus_number)
        active_buses_list.append(current_bus)
    return active_buses_list

def plot_route(locations, bus_number):
    """Plot the route of a specific bus"""
    data = {
        "Time":[],
        "Lat":[],
        "Long":[],
        "Bus number":[]
    }
    bus_route = get_single_bus_route(locations, bus_number)
    for bus in bus_route:
        data["Time"].append(str(bus.time))
        data["Lat"].append(bus.location.latitude)
        data["Long"].append(bus.location.longitude)
        data["Bus number"].append(bus_number)

    fig = px.line_mapbox(data, lat="Lat", lon="Long",
                        hover_data=["Time", "Lat", "Long"], zoom=10,
                        height=800,width=800, color="Bus number")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def calculate_distance(bus1, bus2):
    """Calculate disntance between two recorded instances"""
    coords_1 = (bus1.location.latitude, bus1.location.longitude)
    coords_2 = (bus2.location.latitude, bus2.location.longitude)
    distance = geopy.distance.geodesic(coords_1, coords_2).km
    return distance

def calculate_interval(bus1, bus2):
    """Calculate a time interval between mesurements"""
    return (bus2.time - bus1.time).total_seconds()

def calculate_velocity(bus1, bus2):
    """Calculate bus velocity"""
    distance = calculate_distance(bus1, bus2)
    interval = calculate_interval(bus1, bus2)
    velocity = distance / interval * 3600
    return velocity

def plot_speeding_buses(locations):
    """Plot a scatter map of speeding buses and return the number of them"""
    legal_speed_limit = 50
    # We need to filter anomalies in the form of 'teleporting' buses
    # it is safe to assume that buses can't go faster than 100km/h
    phisical_speed_limit = 100
    number_of_speeding_buses = 0
    data = {
           "Id":[],
           "Lat":[],
           "Long":[],
           "Velocity":[]
    }
    for route in locations:
        prev = None
        counted = False
        for bus in route:
            if prev is None:
                prev = bus
                continue
            # In case the bus is not moving we make sure not to divide by 0
            if calculate_interval(prev, bus) == 0:
                continue

            velocity = calculate_velocity(prev, bus)
            prev = bus
            if phisical_speed_limit > velocity > legal_speed_limit:
                if not counted:
                    counted = True
                    number_of_speeding_buses += 1
                data["Id"].append(bus.bus_id)
                data["Lat"].append(bus.location.latitude)
                data["Long"].append(bus.location.longitude)
                data["Velocity"].append(velocity)

    color_scale = [(0, 'orange'), (1,'red')]
    fig = px.scatter_mapbox(data,
                        lat="Lat",
                        lon="Long",
                        hover_name="Id",
                        hover_data=["Id","Velocity", "Lat", "Long"],
                        color_continuous_scale=color_scale,
                        size="Velocity",
                        color="Velocity",
                        zoom=10,
                        height=800,
                        width=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    return number_of_speeding_buses

def plot_stopped_places(locations):
    """Plot a scatter map of stop locations"""
    data = {
           "Id":[],
           "Lat":[],
           "Long":[],
    }
    for route in locations:
        prev = None
        for bus in route:
            if prev is None:
                prev = bus
                continue
            # In case the bus is not moving we make sure not to divide by 0
            if calculate_interval(prev, bus) == 0:
                continue

            velocity = calculate_velocity(prev, bus)
            prev = bus
            if velocity < 1:
                data["Id"].append(bus.bus_id)
                data["Lat"].append(bus.location.latitude)
                data["Long"].append(bus.location.longitude)

    color_scale = [(0, 'orange'), (1,'red')]
    fig = px.scatter_mapbox(data,
                        lat="Lat",
                        lon="Long",
                        hover_name="Id",
                        hover_data=["Id", "Lat", "Long"],
                        color_continuous_scale=color_scale,
                        zoom=10,
                        height=800,
                        width=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def plot_bus_speeds(locations, min_speed, max_speed):
    """Plot the distribution of bus speeds"""
    data = []
    for route in locations:
        prev = None
        for bus in route:
            if prev is None:
                prev = bus
                continue
            # In case the bus is not moving we make sure not to divide by 0
            if calculate_interval(prev, bus) == 0:
                continue
            velocity = calculate_velocity(prev, bus)
            if max_speed > velocity > min_speed:
                data.append(int(velocity))
            prev = bus
    plt.hist(data, bins=np.arange(min(data), max(data) + 1))

def percent_of_buses_active(locations):
    """Calculate the percentage of active buses"""
    acticve_buses = get_active_numbers(locations)
    acticve_buses_number = len(acticve_buses)
    total_buses_number = len(locations[0])
    return acticve_buses_number / total_buses_number * 100

def percent_of_speed_anomalies(locations):
    """Calculate the percentage of incorrect location data"""
    phisical_speed_limit = 100
    number_of_anomalies = 0
    all_readings = 0
    for route in locations:
        prev = None
        for bus in route:
            if prev is None:
                prev = bus
                continue
            # In case the bus is not moving we make sure not to divide by 0
            if calculate_interval(prev, bus) == 0 :
                continue

            velocity = calculate_velocity(prev, bus)
            prev = bus
            all_readings += 1
            if velocity > phisical_speed_limit:
                number_of_anomalies +=1
    return number_of_anomalies / all_readings * 100
