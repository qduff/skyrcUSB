# basic Prometheus metric server

from flask import Flask, make_response
import skyrcUSB
from skyrcUSB.core import chargeException

app = Flask(__name__)


def get_metrics():
    sides = []
    for i in range(2):
        cstate = app.charger.getChargeData(i, raiseerrors= False)
        sides.append("""
# HELP error Whether there is an error
# TYPE error gauge
error{{side={side}}} {error}

# HELP charge_voltage The current voltage of the charge
# TYPE charge_voltage counter
charge_voltage{{side={side}}} {voltage}

# HELP charge_current The current current of the charge
# TYPE charge_current counter
charge_current{{side={side}}} {current}

# HELP charge_current The current current of the charge
# TYPE charge_current counter
charge_current{{side={side}}} {current}



    """.format(side = i, error = int(cstate.error), voltage =  cstate.voltage , current =  cstate.current ))
        
    return "\n".join(sides)


@app.route('/metrics')
def metrics():
    response = make_response(get_metrics(), 200)
    response.mimetype = "text/plain"
    return response


if __name__ == '__main__':
    app.charger = skyrcUSB.Charger()  # Instantiate object and connect
    app.run(debug=True)

