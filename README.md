# Adam HCB123 lab scale
Program for recording weight vs time on the ADAM-weight (HCB123 Highland series).

## Usage
Connect the ADAM HCB123 to the computer, open a terminal and run _HCB123.py_ \
(To abort the program just press `Ctrl + C` or `Ctrl + Z` at any time.)

The program tryes to autoconnect, if the scale is not found you will get a list of avalable COM-ports to choose from. 
NOTE: The serial port location may varry and is also different between OS's.

_OSX when scale found:_
```
>>> Serial Connection established: /dev/cu.usbserial-1462

**********************
    ADAM HCB123 
**********************
Choose command number:
1 - Show scale reading
2 - Print to file
----------------------
>>> 
```
_OSX when scale not found_
```
ERROR: Did not find any connected ADAM HCB123 devices
       these ports were found:

NUM                             ADDRESS -          MANUFACTURER                     DESCRIPTION  
  0                /dev/cu.lpss-serial1 -                   None                             n/a  
  1                /dev/cu.lpss-serial2 -                   None                             n/a  
  2     /dev/cu.Bluetooth-Incoming-Port -                   None                             n/a  
  3              /dev/cu.usbserial-1462 -                   FTDI                  USB <-> Serial  

Pick the desired port number: 
```
In the code above port nr 3 represent the ADAM HCB123. Just type in 3 in terminal,press enter and you will get the startup screen as in the _scale found_-case.

`1 - Show scale reading` starts pumping out values that the scale records to the terminal, but no data is saved. In order to save data choose
`2 - Print to file`. This prompts the user with: 
```
Choose filename:
>>> 
```
File extension `.txt` is automatically added if not added manually.
If filename already exist data is appended to the file with an empty line. 
e.g. if user set filname to `test` twice the content of `test.txt` would be somthing like:
```
TIME(s)	WEIGHT(g)

0.13	-0.005
0.62	-0.005
1.12	-0.005
1.63	-0.005
2.13	-0.005

TIME(s)	WEIGHT(g)
0.29	-0.005
0.78	-0.005
1.29	-0.005
```


## Requirements
- Python v3.x
- pyserial v3.4+

## Platforms
- OSX: Working
- Windows: Working
- Rasbian: Working
- Linux: Working
