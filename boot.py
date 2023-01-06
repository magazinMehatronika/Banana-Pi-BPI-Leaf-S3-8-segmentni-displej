from machine import Pin, PWM
import time
import sys


#Pin list for digits
pinList = [[1,2,3,4,6,7],[4,6],[1,3,4,5,7],[1,4,5,6,7],[2,4,5,6],[1,2,5,6,7],[1,2,3,5,6,7],[1,4,6],[1,2,3,4,5,6,7],[1,2,4,5,6,7]]

#############
#Driver code#
#############

#Pin setup
for i in range (1,9):
    globals()[f"PWM_LED{i}"] = PWM(Pin(i)) #Global dictionary used for dynamic global variable generation
    globals()[f"PWM_LED{i}"].freq(1000)
    globals()[f"PWM_LED{i}"].duty(0)

#Clear routine
def clearDisplay():
    for i in range (1,9):
        globals()[f"PWM_LED{i}"].duty(0)
    
#Digit display - use when dimming effects or custom timings required
def displayDigit(n, dot, dutyCycle):
    if n in range (0,10) and dot in range (0,2): #Check if arguments in range to prevent variable naming errors
        clearDisplay() #Clear display in case something was displayed before
        for i in pinList[n]:
            globals()[f"PWM_LED{i}"].duty(dutyCycle)
        if dot == 1: #Dot as argument
            PWM_LED8.duty(dutyCycle)
    elif str(n) == '-': #Stringify n for data integrity
        clearDisplay()
        PWM_LED5.duty(dutyCycle)
    else: #If not, safely handle error
         raise Exception("displayDigit error (could be caused by arguments out of bounds or program termination).")
    
#Number display as a wrapper for displayDigit command
def displayNumber(n, dot, dutyCycle, ms, pre_ms=50): #Optional pre_ms argument for predelay settings, automatically set to 50
    try: #Try if int; exception catches for logic if string
        numList = [int(x) for x in str(n)] #Turns an integer into a list of its digits, e.g. 429 -> [4,2,9]
    except ValueError: #If argument is string, do whatever it needs to make above command accept this input
        numList = []
        for x in n:
            try:
                numList.append(int(x))
            except ValueError:
                numList.append(x)
            
    for i in numList: #Iterate through list and pass i as argument into the displayDigit command
        try: #No argument check in wrapper command as subcommand performs these, try method required to pass exception along
            clearDisplay()
            time.sleep_ms(pre_ms)
            displayDigit(i, dot, dutyCycle)
            time.sleep_ms(ms)
        except:
            raise Exception("displayNumber error (could be caused by arguments out of bounds or program termination).")
        
###########
#Main code#
###########


while True:
    displayNumber("17-12-1973",0,1023,750)
