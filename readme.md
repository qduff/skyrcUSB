# skyrcUSB

This is a library which you can use to interface with your skyRC charger. Examples of what it can do is return the voltages of all the cells ( even when not charging) and can also return charge data in real time - to one more decimal point than the display on the charger!

It has only been tested with the D100V2 and will throw an error if it detects a different model. This is only done to ensure your charger is not damaged. I presume the code should work - I simply haven't tested it.

*This library is also not able to write changes to the charger or start charges* 

**Note - this library is released under the MIT license, and therefore includes absolutely no warranty.**

Example usage is below:

```python
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
    print("Charger has not started charging.")

```

Have a look at the ./examples/ directory for examples, although you will likely need to take a look at the source code for more advanced usage (who needs documentation?)

The license can be found in LICENSE.txt
