from __future__ import absolute_import
from __future__ import print_function

import os
import sys

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
import traci.constants as tc
import my_constants as cons
import subprocess

vehID = "CarSur-norte"#ONLY FOR TEST, REAL IDS AUTOGENERATE
vehTypeID = "ModMovTimAut"
edgeID = "185320228#1"


#this to verify the min charge for reroute the vehicle to EVSE
def verifyMinEnergy(vehID):
    actualValue = traci.vehicle.getParameter(vehID, cons.ACTUAL_BATTERY_CAPACITY)
    toEVSE = traci.vehicle.getParameter(vehID, cons.GOING_TO_EVSE)
    print(cons.ACTUAL_BATTERY_CAPACITY +": " + actualValue)
    if float(actualValue) < float(cons.MIN_ENERGY_ROUTE_EVSE) and toEVSE == "false" :
        print("CHANGE TARGET")
        traci.vehicle.changeTarget(vehID, edgeID)
        traci.vehicle.setParameter(vehID, cons.GOING_TO_EVSE, "true")
        traci.vehicle.setStop(vehID, edgeID, pos=40.0, startPos=1.0, laneIndex=0)

#this to verify a vehicle at charging station finished charging process
def verifyChargingFinish(vehID) :
    print("VERIFY FINISH")
    actual_bat_cap = traci.vehicle.getParameter(vehID, cons.ACTUAL_BATTERY_CAPACITY)
    ev_target = traci.vehicle.getParameter(vehID, cons.EV_TARGET)
    max_charging_allow = traci.vehicle.getParameter(vehID, cons.MAX_CHARGING_ALLOW)#porcentaje
    max_bat_capacity = traci.vehicletype.getParameter(vehTypeID, cons.MAX_BAT_CAPACITY)
    max_capacity_value = float(max_bat_capacity) * float(max_charging_allow)
    if float(actual_bat_cap) >= float(max_capacity_value) :
        traci.vehicle.changeTarget(vehID, ev_target)     
        traci.vehicle.setParameter(vehID, cons.GOING_TO_EVSE, "false")   
        traci.vehicle.resume(vehID)

#check EV if finish charging or if is needed a charging
def checkEV(vehID):
    toEVSE = traci.vehicle.getParameter(vehID, cons.GOING_TO_EVSE)
    if toEVSE == "true" :
        if traci.vehicle.isStopped(vehID):
            verifyChargingFinish(vehID)
    else:
        verifyMinEnergy(vehID)   

#Now is only one EV, after this method do a loop for all EV in simulation
def checkEVs():
    checkEV(vehID)
    
# this control the simulation loop
def run():
	traci.init(cons.SUMO_PORT) 
	traci.vehicle.subscribe(vehID, (tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION))
	#traci.simulation.subscribe()
	for step in range(1000):
   		print("step", step)
   		traci.simulationStep()
   		checkEVs()
	traci.close()

# this is the main entry point of this script
if __name__ == "__main__":
	sumoBinary = checkBinary('sumo-gui')
	sumoProcess = subprocess.Popen([sumoBinary, "-c", cons.SUMO_CONFIG, "--remote-port", str(cons.SUMO_PORT)], stdout=sys.stdout, stderr=sys.stderr)
	run()
	
