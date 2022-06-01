class NotTested(Exception):
    def __init__(self, msg='This program has not been tested with your model! Do not use!', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)



def getModel(coretype):
    if coretype == "100131":
        return "D100V2"
    
    elif coretype == "100123":
        raise  NotTested 
        return "D400"
    
    elif coretype == "100097":
        raise  NotTested
        return "D200"
    
    elif coretype == "100089":
        raise  NotTested
        return "D100"

    elif coretype == "100125":
        raise  NotTested
        return "D250"

    elif coretype == "100157":
        raise  NotTested
        return "D260"
    
    else:
        raise Exception
    
def getErrorString(errorcode:int) -> str:
    if errorcode == 1:   errstring = "Input Low"
    elif errorcode == 2:   errstring = "Input High"
    elif errorcode == 3:   errstring = "Connection Break"
    elif errorcode == 4:   errstring = "Cell Connector issue"
    elif errorcode == 5:   errstring = "Main Battery port issue"
    elif errorcode == 6:   errstring = "Capacity Cut"
    elif errorcode == 7:   errstring = "Time Cut"
    elif errorcode == 8:   errstring = "Int.Temperature"
    elif errorcode == 9:   errstring = "Batt.Temperature"
    elif errorcode == 10:  errstring = "Over Load"
    elif errorcode == 11:  errstring = "Battery Reversed"
    elif errorcode == 12:  errstring = "Already Charged"
    elif errorcode == 13:  errstring = "Battery full"
    elif errorcode == 14:  errstring = "Other Error"
    else: errstring = "Unknown error..?"
    return errstring