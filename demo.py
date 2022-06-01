import skyrcUSB

# Get charger info

charger = skyrcUSB.Charger()  # Instantiate object and connect
print(f"Model {charger.model_name} SW:{charger.software_version} \n")


# Get voltages for each cell

for sideID in range(2):
    vcells = charger.getCellInfo(side=sideID)  # Left side
    if vcells:
        print(f"{len(vcells)} Cells in the battery")
        [print(f"Cell {i+1}:  {v}mV") for i, v in enumerate(vcells)]
    else:
        print(f"No Cells on side {chr(65+sideID)}")

# Get charger settings

charger.getSettings()

print(f"\nThe charger is configured to not exceed {charger.maxTemp} C or {charger.maxCapacity} mah\n")


# Get charge data on side B

cstate = charger.getChargeData(1)

if cstate.isError():
    print(f"Error: {cstate.getErrorString()}!!!\n")

if not cstate.isIdle(): # if charger is charging or finished
    print(f"Status: {cstate.getStatusString()}")
    print(f"Voltage: {cstate.voltage} mV")
    print(f"Current: {cstate.current} mA")
    print(f"Capacity: {cstate.capacity} mah")
    print(f"Duration: {cstate.chargeDuration} seconds")
else:
    print("Charger is not charging.")


