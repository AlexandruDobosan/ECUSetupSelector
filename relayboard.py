from typing import List, Any, Union
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo

########IMPORTS#########

import hid
import channel8Relay
import ecu
import driver
import math
import configparser



########GLOBALS#########

config = configparser.ConfigParser()
config.read('settings.ini')

vendorID = int(config['setting']['vendor_id'],16)
productID = int(config['setting']['product_id'],16)
nrSetups = int(config['setting']['nrOfSetups'])
progPowSupply = config['pwSup']['prog_pwSup']
defaultVoltage = float(config['pwSup']['OutVoltage'])
defaultCurrent = float(config['pwSup']['OutCurrent'])
isAdmin = config['pwSup']['isAdmin']
pwSupPort = config['pwSup']['com_pwSup']

if nrSetups ==4:
   OptionList = [
   "ECU Setup 1",
   "ECU Setup 2",
   "ECU Setup 3",
   "ECU Setup 4"
   ]
elif nrSetups == 3:
    OptionList = [
        "ECU Setup 1",
        "ECU Setup 2",
        "ECU Setup 3"
    ]
elif nrSetups == 2:
    OptionList = [
        "ECU Setup 1",
        "ECU Setup 2"
    ]
elif nrSetups == 1:
    OptionList = [
        "ECU Setup 1"
    ]


########Flags######
dropdown =0
setupFlag1 = False
setupFlag2 = False
setupFlag3 = False
setupFlag4 = False
setup1Flags = [0,0,0]
setup2Flags = [0,0,0]
setup3Flags = [0,0,0]
setup4Flags = [0,0,0]
debugFlags  = [0,0,0,0]
sourceFlag = 0
voltageMaximum = 40
currentMaximum = 15


#######BACKEND-FUNCTIONS#######

def isDebugging():
    for flag in debugFlags:
        if flag == 1:
            return True
    return False
"""Checks if any of the setups debug function is running.
   Returns True or False if none are active"""

def ignitionButtonBind(nr):
    global setup1,setup2,setup3,setup4
    genericEcu = ecu.ECU_SETUP(nr)                # Create an ECU object whose number we don't know
    relNr = genericEcu.getIgnitionRelay()         # Get in a variable the number of the ignition relay
    if nr == 1:
        if relay.get_status()[relNr-1] == True:   # Check the if the relay with that specific number is turned on or off
            return 1
        else:
            return 0
    elif nr == 2:
        if relay.get_status()[relNr -1] == True:
            return 1
        else:
            return 0
    elif nr == 3:
        if relay.get_status()[relNr-1 ] == True:
            return 1
        else:
            return 0
    elif nr == 4:
        if relay.get_status()[relNr-1 ] == True:
            return 1
        else:
            return 0
    return False
""" For each of the setups,check that their designated ignition relay is turned on,
    Returns 1 for ON
            0 for OFF
            False for Error
"""


def debugButtonBind(nr):
    global setup1,setup2,setup3,setup4
    genericEcu = ecu.ECU_SETUP(nr)
    relNr = genericEcu.getDebugRelay()
    if nr == 1:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr == 2:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr == 3:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr == 4:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    return False

""" For each of the setups,check that their designated debug relay is turned on,
    Returns 1 for ON
            0 for OFF
            False for Error
"""


def powButtonBind(nr):
    global setup1,setup2,setup3,setup4
    numbers = [setup1.getNumber(),setup2.getNumber(),setup3.getNumber(),setup4.getNumber()]
    for num in numbers:
        if num == nr:
            currSet = num
    genericEcu = ecu.ECU_SETUP(nr)
    relNr = genericEcu.getPowerRelay()
    if nr == 1:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr ==2 :
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr == 3:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    elif nr == 4:
        if relay.get_status()[relNr-1] == True:
            return 1
        else:
            return 0
    else:
        return False

""" For each of the setups,check that their designated power relay is turned on,
    Returns 1 for ON
            0 for OFF
            False for Error
"""


#########
#GUI
#########


def sourceToggle():
    global source_btn,sourceFlag,sourceOk

    if sourceFlag == 0 :
          source.OutputOn()
          sourceFlag = 1
    elif sourceFlag == 1 :
          source.OutputOff()
          sourceFlag = 0
    text = source_btn['text']
    if text =='OFF' :
          source_btn['text'] = 'ON'
    else:
          source_btn['text'] = 'OFF'

def setCurrent():
    if float(amp_entry.get()) < 15:
        source.SetOutputCurrent(float(amp_entry.get()))

def setVoltage():
  if float(volt_entry.get()) < voltageMaximum and float(amp_entry.get()) <currentMaximum:
    source.SetOutputVoltage(float(volt_entry.get()))
    source.SetOutputCurrent(float(amp_entry.get()))

def popupShow():
    pass
    #showinfo("Warning","Power source is not programmable,button disabled.")

def adminPopupShow():
    pass
    #showinfo("Warning","Admin permission is not allowed,voltage and current setting disabled")

def missingRelayPopupShow():
    pass
    #showinfo("Warning","Relay module not detected,ECU panel disabled")

def changeState():
    global toggle_btn
    text = toggle_btn['text']
    if(text == 'OFF'):
        toggle_btn['text'] = 'ON'
    else:
        toggle_btn['text'] = 'OFF'

def powerButtonSwitch():
    global toggle_btn
    if toggle_btn["state"] == "normal":
        toggle_btn["state"] = "disabled"
    else:
        toggle_btn["state"] = "normal"

def another_kl():
    global kl_btn,dropdown,setup1,setup2,setup3,setup4,setup1Flags,setup2Flags,setup3Flags,setup4Flags

    if dropdown == 1:
        if setup1Flags[2] == 0 and powButtonBind(dropdown) == 1:
            setup1.turnIgnitionOn()
            setup1Flags[2] = 1
            if ignitionButtonBind(1) == 1:
                kl_btn.config(relief = "sunken")
        else:
            setup1.turnIgnitionOff()
            setup1Flags[2] = 0
            if ignitionButtonBind(1) == 0:
                kl_btn.config(relief = "raised")

    elif dropdown == 2 :
        if setup2Flags[2] == 0 and powButtonBind(dropdown) == 1:
            setup2.turnIgnitionOn()
            setup2Flags[2] = 1
            kl_btn.config(relief = "sunken")
        else:
            setup2.turnIgnitionOff()
            setup2Flags[2] = 0
            kl_btn.config(relief = "raised")
    elif dropdown == 3:
        if setup3Flags[2] == 0 and powButtonBind(dropdown) == 1:
            setup3.turnIgnitionOn()
            setup3Flags[2] = 1
            kl_btn.config(relief = "sunken")
        else:
            setup3.turnIgnitionOff()
            setup3Flags[2] = 0
            kl_btn.config(relief = "raised")
    elif dropdown == 4:
        if  setup4Flags[2] ==0 and powButtonBind(dropdown) == 1:
            setup4.turnIgnitionOn()
            setup4Flags[2] = 1
            kl_btn.config(relief = "sunken")
        else:
            setup4.turnIgnitionOff()
            setup4Flags[2] = 0
            kl_btn.config(relief = "raised")
"""
GUI Function to toggle on/off the ignition button and it's relay
"""


def toggle():
   global dropdown,setup1,setup2,setup3,setup1Flags,setup2Flags,setup3Flags,setup4Flags
   if dropdown ==1:
       if setup1Flags[0] == 0  :
        setup1.turnPowerOn()
        setup1Flags[0] =1

        if powButtonBind(dropdown) == 1 :
            drop.config(state = "disabled")
            changeState()
            if toggle_btn.config('relief')[-1] == 'sunken':
                toggle_btn.config(relief="raised")
            else:
                toggle_btn.config(relief="sunken")

        debug_btn.config(state = "disabled")
        setup1.turnIgnitionOn()
        setup1Flags[2] =1

        kl_btn.config(relief = "sunken")
        #updateIgnitionBtn()
        kl_btn.config(state="active")
       else:
        setup1.turnPowerOff()
        setup1Flags[0] = 0

        if powButtonBind(dropdown) == 0:
            if isDebugging() == False: drop.config(state = "active")
            changeState()
            if toggle_btn.config('relief')[-1] == 'sunken':
                toggle_btn.config(relief="raised")
            else:
                toggle_btn.config(relief="sunken")

        debug_btn.config(state = "active")
        setup1.turnIgnitionOff()
        setup1Flags[2] = 0
        kl_btn.config(relief = "raised")
        #updateIgnitionBtn()
        kl_btn.config(state="disabled")

   elif dropdown ==2  :
       if setup2Flags[0] == 0:
           setup2.turnPowerOn()
           setup2Flags[0] = 1

           if powButtonBind(dropdown) == 1:
               drop.config(state = "disabled")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")

           debug_btn.config(state = "disabled")
           setup2.turnIgnitionOn()
           setup2Flags[2] = 1
           kl_btn.config(relief = "sunken")
           #updateIgnitionBtn()
           kl_btn.config(state="active")

       else:
           setup2.turnPowerOff()
           setup2Flags[0] = 0

           if powButtonBind(dropdown) == 0:
               drop.config(state="active")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")


           debug_btn.config(state = "active")
           setup2.turnIgnitionOff()
           setup2Flags[2] = 0
           kl_btn.config(relief = "raised")
           #updateIgnitionBtn()
           kl_btn.config(state="disabled")

   elif dropdown == 3 :
       if setup3Flags[0] == 0:
           setup3.turnPowerOn()
           setup3Flags[0] = 1

           if powButtonBind(dropdown) == 1:
               drop.config(state="disabled")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")

           debug_btn.config(state = "disabled")
           setup3.turnIgnitionOn()
           setup3Flags[2] = 1
           kl_btn.config(relief = "sunken")
           #updateIgnitionBtn()
           kl_btn.config(state="active")

       else:
           setup3.turnPowerOff()
           setup3Flags[0] = 0

           if powButtonBind(dropdown) == 0:
               drop.config(state="active")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")

           debug_btn.config(state = "active")
           setup3.turnIgnitionOff()
           setup3Flags[2] = 0
           kl_btn.config(relief = "raised")
           #updateIgnitionBtn()
           kl_btn.config(state="disabled")

   elif dropdown == 4:
       if setup4Flags[0] == 0:
           setup4.turnPowerOn()
           setup4Flags[0] = 1

           if powButtonBind(dropdown) == 1:
               drop.config(state="disabled")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")

           debug_btn.config(state = "disabled")
           setup4.turnIgnitionOn()
           setup4Flags[2] = 1
           kl_btn.config(relief = "sunken")
           #updateIgnitionBtn()
           kl_btn.config(state="active")
       else:
           setup4.turnPowerOff()
           setup4Flags[0] = 0

           if powButtonBind(dropdown) == 0:
               drop.config(state="active")
               changeState()
               if toggle_btn.config('relief')[-1] == 'sunken':
                   toggle_btn.config(relief="raised")
               else:
                   toggle_btn.config(relief="sunken")

           setup4.turnIgnitionOff()
           setup4Flags[2] = 0
           kl_btn.config(relief = "raised")
           #updateIgnitionBtn()
           kl_btn.config(state ="disabled")
"""
GUI Function to toggle on/off the power GUI button and the power relay
"""


def enableDebug():
    global debug_btn,dropdown
    if dropdown == 1:

        if setup1Flags[1] == 0:
            setup1.turnDebugOn()
            setup1Flags[1] = 1
            debugFlags[0] = 1

            if debugButtonBind(dropdown) == 1:
                drop.config(state="disabled")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")

        else:
            setup1.turnDebugOff()
            setup1Flags[1] = 0
            debugFlags[0] = 0

            if debugButtonBind(dropdown) == 0:
                drop.config(state="active")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")

    elif dropdown == 2 :

        if setup2Flags[1] == 0:
            setup2.turnDebugOn()
            setup2Flags[1] = 1
            debugFlags[1] = 1

            if debugButtonBind(dropdown) == 1:
                drop.config(state="disabled")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")


        else:
            setup2.turnDebugOff()
            setup2Flags[1] = 0
            debugFlags[1] = 0

            if debugButtonBind(dropdown) == 0:
                drop.config(state="active")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")

    elif dropdown == 3 :
        if setup3Flags[1] == 0:
            setup3.turnDebugOn()
            setup3Flags[1] = 1
            debugFlags[2] = 1

            if debugButtonBind(dropdown) == 1:
                drop.config(state="disabled")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")

        else:
            setup3.turnDebugOff()
            setup3Flags[1] = 0
            debugFlags[2] = 0

            if debugButtonBind(dropdown) == 0:
                drop.config(state="active")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")

    elif dropdown == 4 :
        if setup4Flags[1] == 0:
            setup4.turnDebugOn()
            setup4Flags[1] = 1
            debugFlags[3] = 1

            if debugButtonBind(dropdown) == 1:
                drop.config(state="disabled")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")


        else:
            setup4.turnDebugOff()
            setup4Flags[1] = 0
            debugFlags[3] = 0

            if debugButtonBind(dropdown) == 0:
                drop.config(state="active")
                updateDebugBtn()
                if debug_btn.config('relief')[-1] == 'sunken':
                    debug_btn.config(relief="raised")
                else:
                    debug_btn.config(relief="sunken")
"""
GUI function for turning on/off debug button and debug relay
"""

def on_closing():
    if messagebox.askokcancel("Quit","Do you want to quit?"):
        gui.destroy()
        source.OutputOff()

def Refresher():
    global voltage_lbl,current_lbl
    updateVoltage(source.GetOutputVoltage())
    updateCurrent(source.GetOutputCurrent())
    gui.after(500,Refresher)
"""
Once every half a second the voltage and current labels are updated with values extracted from
the power source.
"""

def updateVoltage(v):
    text = str(v)

    if text == "False":
        text ="No"
        voltage_lbl.config(text = text)
    else:
        voltage_lbl.config(text = text + " V")

def updateCurrent(a):
    text = str(a)

    if text == "False":
        text = "Feed"
        current_lbl.config(text = text)
    else:
        current_lbl.config(text = text + " A")

def updateDebugBtn():
    global debug_btn
    text = debug_btn['text']
    if text == 'Debug ON':
        debug_btn['text'] = 'Debug OFF'
    else:
        debug_btn['text'] = 'Debug ON'

def updateIgnitionBtn():
    global kl_btn
    text = kl_btn['text']
    if text == 'KL_15 ON':
        kl_btn['text'] = 'KL_15 OFF'
    else:
        kl_btn['text'] = 'KL_15 ON'

def changeDropdown(*args):
    global dropdown,setupFlag1,setupFlag2,setupFlag3,setupFlag4
    dropdown = int(variable.get()[10])

    if dropdown == 1:                        # when choosing an option from the dropdown
        setupFlag1 = True                    # all other options are turned off
        setupFlag2 = False
        setupFlag3 = False
        setupFlag4 = False
        setup2.wipeSetup()
        setup2.turnIgnitionOff()
        setup3.wipeSetup()
        setup3.turnIgnitionOff()
        setup4.wipeSetup()
        setup4.turnIgnitionOff()
        kl_btn.config(relief = "raised")     # necessary visual changes are done
        debug_btn.config(relief = "raised",state="active")
        toggle_btn["state"] = "active"
    elif dropdown == 2:
        setupFlag1 = False
        setupFlag2 = True
        setupFlag3 = False
        setupFlag4 = False
        setup1.wipeSetup()
        setup1.turnIgnitionOff()
        setup3.wipeSetup()
        setup3.turnIgnitionOff()
        setup4.wipeSetup()
        setup4.turnIgnitionOff()
        kl_btn.config(relief = "raised")
        debug_btn.config(relief = "raised",state="active")
        toggle_btn["state"] = "active"
    elif dropdown == 3:
        setupFlag1 = False
        setupFlag2 = False
        setupFlag3 = True
        setupFlag4 = False
        setup1.wipeSetup()
        setup1.turnIgnitionOff()
        setup2.wipeSetup()
        setup2.turnIgnitionOff()
        setup4.wipeSetup()
        setup4.turnIgnitionOff()
        kl_btn.config(relief = "raised")
        debug_btn.config(relief = "raised",state="active")
        toggle_btn["state"] = "active"
    elif dropdown == 4:
        setupFlag1 = False
        setupFlag2 = False
        setupFlag3 = False
        setupFlag4 = True
        setup1.wipeSetup()
        setup1.turnIgnitionOff()
        setup2.wipeSetup()
        setup2.turnIgnitionOff()
        setup3.wipeSetup()
        setup3.turnIgnitionOff()
        kl_btn.config(relief = "raised")
        debug_btn.config(relief = "raised",state="active")
        toggle_btn["state"] = "active"


gui = Tk()
gui.title('Setup Selector')
gui.geometry("420x320")
gui.protocol("WM_DELETE_WINDOW",on_closing)
gui.resizable(0,0)

variable = StringVar(gui)
variable.set(OptionList[0])
currentSetup = int(variable.get()[10])

consumption_frame = Frame(master=gui,width =400, height = 120,highlightbackground='black',highlightthickness=1)
consumption_frame.pack()

setting_frame = Frame(master=gui,width=400, height=100,highlightbackground="black",highlightthickness=1)
setting_frame.pack()

selector_frame = Frame(master=gui,width=400,height =100,highlightbackground="black",highlightthickness=1)
selector_frame.pack()

dropbutton_frame = Frame(master = gui,highlightbackground='black',highlightthickness=1)
button_frame = Frame(master= dropbutton_frame,relief=RIDGE)

consumption_lbl = Label(master = consumption_frame,text = "Consumption for the selected ECU")
voltage_lbl = Label(master=consumption_frame,text = "13.5 V",relief = GROOVE,width =6,height=1,font=(None,20),pady=4)
current_lbl = Label(master = consumption_frame,text ="0.5 A",relief = GROOVE,width = 6,height=1,font=(None,20),pady=4)
setConsumption_lbl = Label(master=consumption_frame,text ="Set consumption")

volt_entry = Entry(master=setting_frame,width=6,font=(None,13))
amp_entry = Entry(master=setting_frame,width=6,font=(None,13))
setButton = Button(master = setting_frame,text = "Set",width=12,font=(None,14),relief = RAISED,command = setVoltage)
volt_entry_lbl = Label(master = setting_frame,text = "V",relief = GROOVE,font=(None,13))
amp_entry_lbl = Label(master= setting_frame,text= "A",relief=GROOVE,font=(None,13))

volt_entry.insert(0,defaultVoltage)
amp_entry.insert(0,defaultCurrent)

voltage1Label = Label(master=setting_frame,text="Voltage")
amper1Label = Label(master= setting_frame,text="Current")

voltageLabel = Label(master =consumption_frame,text = "Voltage")
currentLabel = Label(master = consumption_frame,text="Current")

toggle_btn = Button(master=selector_frame,text="OFF", width=12, relief="raised",command = toggle,padx=3,state="disabled",font=(None,12))
debug_btn = Button(master = selector_frame, text ="Debug", width =10, relief = RIDGE,command=enableDebug,padx=3,font=(None,12))
debug_btn.config(state="disabled")
kl_btn = Button(master = selector_frame,text ="KL_15",width=10,relief = RIDGE,command=another_kl,padx=3,font=(None,12))
kl_btn.config(state="disabled")
source_btn = Button(master= consumption_frame,text="POWER\nOFF",width=6,height=2,font=(None,15),relief="raised",padx=3,command = sourceToggle)

drop =OptionMenu(selector_frame,variable,*OptionList)
drop.config(width=25,font=(None,13))
variable.trace('w',changeDropdown)

###
if isAdmin == "false" :                       # admin settings denied,disabled voltage/current setting option

    volt_entry.config(state="disabled")
    amp_entry.config(state="disabled")
    setButton.config(state="disabled")

    adminPopupShow()

if progPowSupply == "false" :                 # power supply is not programmable, disable power supply panel
    source_btn.config(state = "disabled")
    voltage_lbl.config(text="0 V",state="disabled")
    current_lbl.config(text="0 A",state="disabled")
    volt_entry.config(state="disabled")
    amp_entry.config(state="disabled")
    setButton.config(state="disabled")
    popupShow()

consumption_lbl.place(x=100,y=5)
source_btn.place(x=25,y=35)
voltage_lbl.place(x=180,y=35)
current_lbl.place(x=280,y=35)
voltageLabel.place(x=180,y=78)
currentLabel.place(x=280,y=78)

setButton.place(x=220,y=30)

voltage1Label.place(x=80,y=20)
amper1Label.place(x=80,y=50)
volt_entry.place(x=130,y=20)
amp_entry.place(x=130,y= 50)
volt_entry_lbl.place(x=180,y=20)
amp_entry_lbl.place(x=180,y=50)

drop.place(x=70,y=15)
toggle_btn.place(x=30,y=60)
debug_btn.place(x=160,y=60)
kl_btn.place(x=270,y=60)

if __name__ == '__main__':
    from time import sleep
    import configparser
    import driver

    source = driver.HCS()
    source.ClosePort()


    if (source.OpenPort(pwSupPort)):               # if power supply source found ,set the default values for entry fields
        source.SetOutputVoltage(defaultVoltage)
        source.SetOutputCurrent(defaultCurrent)
    else:
        source_btn.config(state = "disabled")

    try:
        relay = channel8Relay.Relay(vendorID,productID)
        setup1 = ecu.ECU_SETUP(1)
        setup2 = ecu.ECU_SETUP(2)
        setup3 = ecu.ECU_SETUP(3)
        setup4 = ecu.ECU_SETUP(4)
    except OSError:
        missingRelayPopupShow()
        drop.config(state='disabled')

    Refresher()
    gui.mainloop()

    try:
        relay.state(0,on = False)
        sleep(5)
    except NameError:
        print()



