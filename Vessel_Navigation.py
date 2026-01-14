import random, math

# Q1: Set the Horizon: Define the World

# Defining global variables
MIN_LAT = -90 # in degree
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180
EARTH_RADIUS = 6378 # in km
STORM_STEPS = 5
UP_RANDOM = 1 # upper and lower limits for the random number in Q6
LOW_RANDOM = -1
UP_SCALE = 2 # upper and lower limits for scale in Q8
LOW_SCALE = 1
CHANCE_OF_WAVE = 0.2
MIN_DISTANCE = 10 # in km


# Q2: Calibrate the Compass: Degrees to Radians

def degrees_to_radians(degrees):
    """
    (float) -> float
    Takes a float number corresponding to an angle in degrees and
    returns its corresponding value in radians rounded to 2 decimals.
    
    Parameter:
        degrees: a float number
    
    Examples:
    >>> degrees_to_radians(180)
    3.14
    >>> degrees_to_radians(360)
    6.28
    >>> degrees_to_radians(10)
    0.17
    """
    
    radians = degrees * math.pi/180
    
    return round(radians, 2)


# Q3: Acquire a Fix: Validate a Coordinate

def get_valid_coordinate(val_name, min_float, max_float):
    """
    (string, float, float) -> float
    Asks the user for a float value until its value is within
    the (min_float, max_float) interval. Returns the value.
    
    Parameters:
        val_name: a string
        min_float: a float number
        max_float: a float number
        
    Examples:
    >>> get_valid_coordinate('x-coordinate', 0, 10)
      What is your x-coordinate ?-1
      Invalid x-coordinate
      What is your x-coordinate ?7.5
    7.5
    
    >>> get_valid_coordinate('y-coordinate', -30, 30)
      What is your y-coordinate ?-50
      Invalid y-coordinate
      What is your y-coordinate ?45
      Invalid y-coordinate
      What is your y-coordinate ?0.3
    0.3
    
    >>> get_valid_coordinate('longitude', -180, 180)
      What is your longitude ?-20
    -20
    
    """

    in_interval = False
    
    while not in_interval:
        # Defining input question
        val_question = "What is your " + val_name + " ?"
        value = float(input(val_question))
    
        # Checking if it's within the interval
        if min_float < value < max_float:
            return value
    
        else:
            print("Invalid",val_name)

 
 # Q4: Plot Our Position: Get GPS Location
 
def get_gps_location():
    """
    () -> (float, float)
    Calls get_valid_coordinate to get the latitude and longitude values
    of the vessel. Returns two floats for the coordinates of the vessel.
    
    Parameters: None
    
    Examples:
    >>> get_gps_location()
      What is your latitude ?45.51
      What is your longitude ?-73.56
    (45.51, -73.56)
    
    >>> get_gps_location()
      What is your latitude ?120
      Invalid latitude
      What is your latitude ?80
      What is your longitude ?-180
      Invalid longitude
      What is your longitude ?-23
    (80.0, -23.0)
    
    >>> get_gps_location()
      What is your latitude ?0.0
      What is your longitude ?185
      Invalid longitude
      What is your longitude ?0.0
    (0.0, 0.0)
    
    """
    latitude = get_valid_coordinate('latitude', MIN_LAT, MAX_LAT)
    longitude = get_valid_coordinate('longitude', MIN_LONG, MAX_LONG)
    
    return (latitude, longitude)


# Q5: Chart the Distance: Great-circle Calculator

def distance_two_points(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    (float, float, float, float) -> float
    Takes four float inputs and returns the distance between two locations
    based on the Haversine formula.
    
    Parameters:
    latitude_1: a float number
    longitude_1: a float number
    latitude_2: a float number
    longitude_2: a float number
    
    Examples:
    >>> distance_two_points(45.508888, -73.561668, 19.432608, -99.133209)
    3723.31 km
    >>> distance_two_points(5.5, 5.5, 5.5, 5.5)
    0.0 km
    >>> distance_two_points(80, 170, -80, -170)
    17890.7 km
    
    """
    
    # Converting degree values to radians
    latitude_1 = degrees_to_radians(latitude_1)
    longitude_1 = degrees_to_radians(longitude_1)
    latitude_2 = degrees_to_radians(latitude_2)
    longitude_2 = degrees_to_radians(longitude_2)
    
    # Calculating the difference between latitudes and longitudes
    delta_lat = abs(latitude_1 - latitude_2)
    delta_long = abs(longitude_1 - longitude_2)
    
    # Computing the distance using the Haversine formula
    a = math.pow(math.sin(delta_lat/2),2) + math.cos(latitude_1) * \
        math.cos(latitude_2) * math.pow(math.sin(delta_long/2),2)
    c = 2 * math.atan2(math.pow(a,1/2),math.pow(1-a,1/2))
    distance = round(EARTH_RADIUS * c, 2)
    
    return distance


# Q6: Helm Nudge: Apply Wave Impact to a Coordinate

def apply_wave_impact(position, min_float, max_float):
    """
    (float, float, float) -> float
    Takes an intial position and returns a new position within the range.
    
    Parameters:
    position: a float number
    min_float: a float number
    max_float: a float number
    
    Examples:
    >>> apply_wave_impact(0, -5, 5)
    -0.9
    >>> apply_wave_impact(0, -10, 10)
    0.38
    >>> apply_wave_impact(0, -10, 10)
    -0.98
    
    """
    
    in_interval = False
    
    while not in_interval:
        # Converting random number to a step in the range [-1,1)
        random_num = LOW_RANDOM - (LOW_RANDOM - UP_RANDOM) * random.random()
        new_position = position + random_num
        
        # Checking if it's within the interval
        if min_float < new_position < max_float:
            return round(new_position, 2)
        
        
# Q7: Wave Hit Event: Reorient and Recheck

def wave_hit_vessel(latitude, longitude):
    """
    (float, float) -> (float, float)
    Returns the new coordinates of a vessel after being hit by a wave.
    
    Parameters:
    latitude: a float number
    longitude: a float number
    
    Examples:
    >>> wave_hit_vessel(80, -17)
    (79.1, -17.83)
    >>> wave_hit_vessel(50, 60)
    (49.58, 59.97)
    >>> wave_hit_vessel(-30, -100)
    (-29.35, -100.41)
    
    """
    
    new_latitude = apply_wave_impact(latitude, MIN_LAT, MAX_LAT)
    new_longitude = apply_wave_impact(longitude, MIN_LONG, MAX_LONG)
    
    return (new_latitude, new_longitude)


# Q8: Helm Advance: Move Toward Waypoint

def move_toward_waypoint(current_lat, current_long, wayp_lat, wayp_long):
    """
    (float, float, float, float) -> (float, float)
    Returns new coordinates of a vessel moving towards waypoint.
    
    Parameters:
    current_lat: a float number
    current_long: a float number
    wayp_lat: a float number
    wayp_long: a float number
    
    Examples:
    >>> move_toward_waypoint(0, 0, 5, 5)
    (2.7, 2.7)
    >>> move_toward_waypoint(89, 179, 90, 180)
    (89.52, 179.52)
    >>> move_toward_waypoint(-30, -50, 90, 180)
    (30.82, 66.56)
    """
    
    # Converting scale to the range [1,2)
    scale = LOW_SCALE - (LOW_SCALE - UP_SCALE) * random.random()
    
    # New coordinates
    new_lat = current_lat + (wayp_lat - current_lat) / scale
    new_long = current_long + (wayp_long - current_long) / scale
    
    # Checking if any value goes past a boundary. If yes, set to boundary value
    if new_lat < MIN_LAT and MIN_LONG <= new_long <= MAX_LONG:
        return (MIN_LAT, round(new_long, 2))
    
    elif new_lat > MAX_LAT and MIN_LONG <= new_long <= MAX_LONG:
        return (MAX_LAT, round(new_long, 2))
    
    elif MIN_LAT <= new_lat <= MAX_LAT and new_long < MIN_LONG:
        return (round(new_lat, 2), MIN_LONG)
    
    elif MIN_LAT <= new_lat <= MAX_LAT and new_long > MAX_LONG:
        return (round(new_lat, 2), MAX_LONG)
    
    else:
        return (round(new_lat, 2), round(new_long, 2))
    

# Q9: Bridge Console: Storm Run to Waypoint

def vessel_menu():
    """
    (None) -> None
    Asks the user to input the vessel's starting location.
    
    Displays a menu of options that lets the captain set a waypoint, move
    towards it while reporting status, or exit.
    
    The interactive loop continues until the mission succeeds, fails due to
    a storm, or the captain exits.
    """
    
    # Defining variables
    storm_count = STORM_STEPS
    waypoint_entered = False
    choice = 0
    
    # Welcome message
    print("Welcome to the boat menu!")
    
    # Getting starting location
    latitude, longitude = get_gps_location()
    
    menu = "Please select an option below: \n\
1) Set waypoint \n\
2) Move toward waypoint and Status report \n\
3) Exit boat menu "
    
    
    while choice != 3:
        print(menu)
        choice = int(input("Choose:"))
        
        # Set Waypoint
        if choice == 1:
            print("Enter waypoint coordinates.")
            waypoint_lat, waypoint_long = get_gps_location()
            print("Waypoint set to latitude of", waypoint_lat,\
                  "and longitude of", waypoint_long)
            waypoint_entered = True
        
        # Move Toward Waypoint & Report Status
        elif choice == 2:
            # Checking if user set waypoint
            if waypoint_entered:
                print("Captain Log: Journeyed towards waypoint.")
                
                # Moving towards waypoint
                latitude, longitude = move_toward_waypoint(latitude,\
                                                           longitude,\
                                                           waypoint_lat,\
                                                           waypoint_long)
                # Chance of being hit by a wave
                if random.random() < CHANCE_OF_WAVE:
                    latitude, longitude = wave_hit_vessel(latitude, longitude)
                    print("Captain Log: Wave impact recorded.")
        
                # Updating current position
                print("Current position is latitude of", latitude,\
                      "and longitude of", longitude)
        
                # Distance to waypoint
                distance = distance_two_points(latitude, longitude,\
                                               waypoint_lat, waypoint_long)
                print("Distance to waypoint:", distance, "km")
        
                # Checking for end conditions
                
                # Checking if waypoint is reached
                if distance <= MIN_DISTANCE:
                    print("Mission success: waypoint reached before storm.")
                    choice = 3 # Terminates function
        
                # Checking if storm has arrived
                else:
                    storm_count -= 1
                    print("Storm T-minus:", storm_count)
                    if storm_count == 0:
                        print("Mission failed: storm hit before arrival.")
                        choice = 3 
                
            else:
                print("No waypoint set.")
                
        # Exit Console
        elif choice == 3:
            print("Console closed by captain.")
    
    