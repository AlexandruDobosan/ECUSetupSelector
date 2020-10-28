# ECU Setup Selector

ECU Setup Selector is a software application designed in python for switching ECU setups via a GUI without the need to change hardware.



## Installation

1.Build python develop environment:
	1.1 install python2 or python3 into windows.https://www.python.org/downloads/ choose one for windows.





2.Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyserial, configparser and hidapi libraries.

```bash
pip install pyserial
```

```bash
pip install hidapi
```

````bash
pip install configparser
````



## GUI




> **Usage**:
>
> > - **Power OFF/Power ON **
> >
> >   > Is a switch type button that enables/disables the output on the programmable power source
> >
> > - **Set** 
> >
> >   > When pressed sends the values in the entry boxes to be outputted by the programmable power source,0 values should never be sent by the user as it could generate abnormal behavior , there is an upper limit to both voltage and current values that is hardcoded in settings.ini file
> >
> > - **ECU Setup Selection Dropdown List** 
> >
> >   > Dropdown list from which the user selects a setup. Inactive when any setup's buttons are pressed
> >
> > - **OFF/ON**
> >
> >   > Is a switch type button that enables/disables power for the selected ECU setup,also enables/disables **KL_15** button
> >
> > - **Debug ON/OFF** 
> >
> >   >Is a switch type button that enables/disables the debugger for the selected ECU setup,inactive when power button is switched on,otherwise independent 
> >
> > - **KL_15 ON/OFF**
> >
> >   > **KL_15** or **Ignition** is a switch type button that enables/disables the ignition for the selected ECU,inactive when power button is switched off

