# WifiSignalSimulator
#
# Models the loss of signal strength of WiFi devices in range of
# two Access Points (APs) while on a high-speed train.
#
# Author: Devin Ekins
# Contact: DevinJ.Ekins@gmail.com
#
#
# Inputs:
# - Distance, in meters, between AP 1 and AP 2
# - Distance, in meters, between Train and AP 1
# - Velocity of Train in meters per second.
#
# Assumptions: 
# - Train is experiencing no acceleration of any kind.
# - Train is directly "beneath" AP 1 initially in the y dimension.
# - Train always occupies the same plane of depth (z-axis) as both APs.
# - Train track runs parallel to the APs. (No change in the y coordinate.)
# - Free space loss is the only factor determining signal loss.
#
# Outputs:
# - Two lists of dB values separated over 1 ms time intervals, covering 5 seconds.
#   Each value will be rounded to three decimal places.
#   The first line will correspond to signal loss with respect to AP 1.
#   The second line will correspond to signal loss with respect to AP 2.

import sys
from math import hypot, log10

def current_signal_distance(AP_number, starting_train_distance, inter_AP_distance, time, velocity):
    '''Returns the distance between the train and the given AP, indicated
    by its number, at this point in time.
    Inputs:
        - AP_number: 1 or 2
        - starting_train_distance: Distance, in meters between the train's
          initial position and AP 1.
        - inter_AP_distance: Distance, in meters between the two APs.
        - time: time elapsed in seconds.
        - velocity: speed of train in meters per second.
    Output:
        - distance in meters.'''
    if AP_number == 1:
        a = starting_train_distance
        b = velocity * time
        return hypot(a, b)
    elif AP_number == 2:
        a = starting_train_distance
        b = inter_AP_distance - velocity * time
        return hypot(a, b)
    else:
        raise ValueError(str(AP_number) + " must be either 1 or 2.")

def compute_free_space_loss(distance, band="2.4"):
    '''Returns the freespace loss in dB, given a particular distance.
    Assumes the 2.4 GHz WiFi band  by default.
    Inputs:
        distance - integer distance to AP in meters.
        band - optional string representing WiFi frequency in Gigahertz.
               Legal Values: "2.4", "5.0"
    Output:
        Decibels of free space loss as a float.'''
    wavelength = None
    if band == "2.4":
        wavelength = 0.12491 # meters
    elif band == "5.0":
        wavelength = 0.05996 # meters
    else:
        raise ValueError(str(band) + " is an unsupported frequency or is incorrectly formatted.")
    constant_factor = 21.984 # log10((4pi)^2) rounded to three digits.
    return -20 * log10(wavelength) + 20 * log10(distance) + constant_factor
        
def main(ap_distance, train_distance, train_velocity, granularity=0.001, sample_count=5000, mantissa_length=3):
    '''As stated at top of file.
    Default granularity is 1 millisecond.
    Default samples is 5000, starting with time = 0.
    Default number of digits of mantissa is 3.'''
    format_string = "{0:." + str(mantissa_length) + "f}"
    AP1_signal_losses = []
    AP2_signal_losses = []
    for t in range(0, sample_count):
        time = float(t) * granularity
        AP1_distance = current_signal_distance(1, train_distance, ap_distance, time, train_velocity)    
        AP1_signal_loss = format_string.format(compute_free_space_loss(AP1_distance))
        AP1_signal_losses.append(AP1_signal_loss)
        AP2_distance = current_signal_distance(2, train_distance, ap_distance, time, train_velocity)
        AP2_signal_loss = format_string.format(compute_free_space_loss(AP2_distance))
        AP2_signal_losses.append(AP2_signal_loss)
    
    with open("wifi_signal_simulator.out", "w") as f:
        for loss in AP1_signal_losses:
            f.write(loss + " ")
        f.write("\n")
        for loss in AP2_signal_losses:
            f.write(loss + " " )
    sys.exit(0)
    
def usage():
    '''Poor man's usage function.'''
    print "Usage: \n"
    print str(sys.argv[0]) + " <inter-AP-distance> <train-AP-distance> <train-velocity>"
    print "Suggested values for execution: "
    print str(sys.argv[0]) + " 100 10 92"
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    try:
        main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    except ValueError as v:
        usage()
        raise v
        