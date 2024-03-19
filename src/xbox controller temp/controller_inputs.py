from xbox_controller import XInput
from time import sleep
import re

#Extracts values from inputs and put them in an int list
'''def listOfIntInputs (inputString):
    numberMatches = map(lambda num: int(num),re.findall("-?\d+" ,inputString)) 
    return list(numberMatches)  


xi = XInput()
activity = 0
'''
#inputListString = str(xi.GetState(0)) #store string inputs
#print(inputListString)
'''while True:
    inputListString = str(xi.GetState(0)) #store string inputs
    inputValueList = listOfIntInputs(inputListString)

    if activity != inputValueList[0]: #if controller used, print values of inputs (this is where to s)
        print(inputValueList)
        #tell PWM to go to certain values
        #send HIGH or LOW

    activity = inputValueList[0]
    sleep(0.016)
'''
#need to implement deadzones and

class XboxInputsWrapper():
    xi = XInput()
    intList = 0
    deadZone = 0.10
    analogStickMax = 32768
    def read(self):
        intList = self.toIntList(str(self.xi.GetState(0)))
        self.intList = intList
        return intList
    def toIntList(self, inputString):
        numberMatches = map(lambda num: int(num),re.findall("-?\d+" ,inputString))
        return list(numberMatches)
    def OutsideDeadZoneCheck(self):
        results = []
        for i in self.intList[-4:]:
            if abs(i) < self.analogStickMax*self.deadZone:
                results.append(True)
            else:
                results.append(False)
        return results.__contains__(False)
    def TriggerPressurePercent(self):
        Rtrigger = round(self.intList[-6]/255,3)
        Ltrigger = round(self.intList[-5]/255,3)
        return (Rtrigger, Ltrigger)
    def AnalogPercentages(self):
        deadRange = self.analogStickMax*self.deadZone
        activeRange = self.analogStickMax-deadRange
        analogValues = self.intList[-4:]
        percentsList = []
        for i in range(4):
            percentsList.append(round((abs(analogValues[i])-deadRange)/activeRange, 3) if abs(analogValues[i]) > deadRange else 0)
            percentsList[i] = percentsList[i] if analogValues[i]>0 else -percentsList[i]
        return {"LX":percentsList[0],"LY":percentsList[1],"RX":percentsList[2],"RY":percentsList[3]}

#Testing and usage examples
XController = XboxInputsWrapper()

while True: #Game/Life loop
    XInputVals = XController.read()
    outsideDeadzone = XController.OutsideDeadZoneCheck()
    triggerPressures = XController.TriggerPressurePercent()
    analogPercent = XController.AnalogPercentages()
    jsonout = {"xinputvals": XInputVals,
               "outsidedeadzone": outsideDeadzone,
               "triggerpressures": triggerPressures,
               "analogpercent": analogPercent}
    print(XInputVals)
    print(outsideDeadzone)
    print(triggerPressures)
    print(analogPercent)
    sleep(0.5)