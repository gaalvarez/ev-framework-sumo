#!/usr/bin/env python
# encoding: utf-8
"""
my_constants.py
"""

SUMO_PORT = 8876
MIN_ENERGY_ROUTE_EVSE = 1000

#PATH OF CONFIGURATION FILES OF SUMO
SUMO_CONFIG="prueba.sumo"

#PARAMS NAMES FOR DESCRIPTIVE FILES SUMO
ACTUAL_BATTERY_CAPACITY = "actualBatteryCapacity"
GOING_TO_EVSE="toEVSE" #bool for indicate if the vehicle is going to EVSE
EV_TARGET="ev_target" #destination of EV
MAX_CHARGING_ALLOW="max_charging_cap" #max capacity for charging in EVSE (0-1) (%)
MAX_BAT_CAPACITY="maximumBatteryCapacity"

