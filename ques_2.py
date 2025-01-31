import math
from geopy.distance import geodesic
import matplotlib.pyplot as plt
# from dronekit import connect, VehicleMode, LocationGlobalRelative
# import time


waypoints = [
    {'lat': 37.7749, 'lon': -122.4194, 'alt': 30}, 
    {'lat': 37.7755, 'lon': -122.4180, 'alt': 40},  
    {'lat': 37.7760, 'lon': -122.4165, 'alt': 50},  
    {'lat': 37.7765, 'lon': -122.4150, 'alt': 60},  
    {'lat': 37.7770, 'lon': -122.4135, 'alt': 70},  
    {'lat': 37.7775, 'lon': -122.4120, 'alt': 80},  
    {'lat': 37.7780, 'lon': -122.4105, 'alt': 90},  
    {'lat': 37.7785, 'lon': -122.4090, 'alt': 100}, 
    {'lat': 37.7790, 'lon': -122.4075, 'alt': 110}, 
    {'lat': 37.7795, 'lon': -122.4060, 'alt': 120}, 
    {'lat': 37.7800, 'lon': -122.4045, 'alt': 130}, 
    {'lat': 37.7805, 'lon': -122.4030, 'alt': 140}, 
    {'lat': 37.7810, 'lon': -122.4015, 'alt': 150}, 
    {'lat': 37.7815, 'lon': -122.4000, 'alt': 160},
    {'lat': 37.7820, 'lon': -122.3985, 'alt': 10}   
]


def calculate_perpendicular_waypoint(currentPoint, nextPoint):
    
    dx = nextPoint['lon'] - currentPoint['lon']
    dy = nextPoint['lat'] - currentPoint['lat']
    perp_dx = -dy
    perp_dy = dx
    magnitude = math.sqrt(perp_dx**2 + perp_dy**2)
    perp_dx /= magnitude
    perp_dy /= magnitude
    
    # Scale to 100 meters (approximate conversion to degrees)
    scale = 100 / 111320  # 1 degree ≈ 111,320 meters
    new_lat = currentPoint['lat'] + perp_dy * scale
    new_lon = currentPoint['lon'] + perp_dx * scale
    
    return {'lat': new_lat, 'lon': new_lon, 'alt': currentPoint['alt']}

# Insert the new waypoint after 10 waypoints
if len(waypoints) >= 10:
    new_wp = calculate_perpendicular_waypoint(waypoints[9], waypoints[10])
    waypoints.insert(10, new_wp)


def calculate_distance(wp1, wp2):
    return geodesic((wp1['lat'], wp1['lon']), (wp2['lat'], wp2['lon'])).meters

def estimate_time(distance, speed=10):  # Speed in m/s
    return distance / speed

total_distance = 0
for i in range(len(waypoints) - 1):
    distance = calculate_distance(waypoints[i], waypoints[i + 1])
    total_distance += distance
    time_est = estimate_time(distance)
    print(f"Waypoint {i+1} to {i+2}: Distance = {distance:.2f}m, Time = {time_est:.2f}s")

print(f"Total distance: {total_distance:.2f}m")


lats = [wp['lat'] for wp in waypoints]
lons = [wp['lon'] for wp in waypoints]
alts = [wp['alt'] for wp in waypoints]

# Create a figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

#  lat vs. lon
axes[0].plot(lons, lats, marker='o', linestyle='-', color='b')
axes[0].scatter(lons[0], lats[0], color='g', s=100, label='Start')
axes[0].scatter(lons[-1], lats[-1], color='r', s=100, label='End')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
axes[0].set_title('Latitude vs. Longitude')
axes[0].legend()
axes[0].grid(True)

#  lat vs. alt
axes[1].plot(lats, alts, marker='o', linestyle='-', color='b')
axes[1].scatter(lats[0], alts[0], color='g', s=100, label='Start')
axes[1].scatter(lats[-1], alts[-1], color='r', s=100, label='End')
axes[1].set_xlabel('Latitude')
axes[1].set_ylabel('Altitude (m)')
axes[1].set_title('Latitude vs. Altitude')
axes[1].legend()
axes[1].grid(True)

# lon vs. alt
axes[2].plot(lons, alts, marker='o', linestyle='-', color='b')
axes[2].scatter(lons[0], alts[0], color='g', s=100, label='Start')
axes[2].scatter(lons[-1], alts[-1], color='r', s=100, label='End')
axes[2].set_xlabel('Longitude')
axes[2].set_ylabel('Altitude (m)')
axes[2].set_title('Longitude vs. Altitude')
axes[2].legend()
axes[2].grid(True)

# Adjust layout and show the plots
plt.tight_layout()
plt.show()

## plots in 3d
# lats = [wp['lat'] for wp in waypoints]
# lons = [wp['lon'] for wp in waypoints]
# alts = [wp['alt'] for wp in waypoints]

# # Create a 3D plot
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')

# # Plot the path
# ax.plot(lons, lats, alts, marker='o', linestyle='-', color='b', label='Path')

# # Mark the start and end points
# ax.scatter(lons[0], lats[0], alts[0], color='g', s=100, label='Start')
# ax.scatter(lons[-1], lats[-1], alts[-1], color='r', s=100, label='End')

# # Add labels and title
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# ax.set_zlabel('Altitude (m)')
# ax.set_title('3D Drone Mission Path')
# ax.legend()

# # Show the plot
# plt.show()