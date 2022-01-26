# rokenbok-controller-port
This is a repo for using an Arduino to control a Rokenbok and general documentation on how the controller ports work. This repo includes a way to control by a singular keyboard or multiple controllers. 

The goal of this Readme is only to explain how to set up the Arduino(s), run my scripts and layout a roadmap for future development. You can find my actual documentation on how the original controllers function and communicate with the Command Deck [here.](Documentation/controller-port.md)



# Installation/Setup
### Hardware

The Arduino will use the following ports:

Serial Clock - Digital 2

Latch - Digital 3

Data - Digital 4

Ground the Ground line from the Command Deck into the Arduino

Put the VCC into any port you like.

You can find details on the Arduino to Command Deck connections [here](Documentation/Connections.png) and the pinout for the DB9 connector [here.](Documentation/Controller-Pinout.txt)


### Software
Upload the 'Hackenbok.ino' sketch to the Arduino(s). Neccesary adjustments listed in the top of 'Hackenbok.ino' 

Run Controller.exe

Alternatively, if you wish to run and edit the script.

Required Library:

```pip install pyserial```

For controllers support:

```pip install pygame```

For keyboard control:

```pip install pywin32```

1. After getting the libraries, upload the 'Hackenbock.ino' sketch to the Arduino(s). Adjust the sketch as needed depending on the model. 

2. Run Controller.py or Keyboard.py

4. Play Rokenbok!

### TO DO:

#### Efficiency:
1. Fix incredibly inefficient controller file 
   - refactor main loop. currently copy pasted for each controller instead of in a function
2. Make Arduino code shift bits. Actually emulate the bytes sent on the original controller
   - Currently just telling it to spike on the right clock if a button is presesed. 
   - This is much less efficient then just reading each bit in a byte. I'll explain below.

#### Functionality: 

1. Add R and L trigger (This one's easy, I've just been lazy and these buttons are not frequently used)
2. Compile into executable
3. ~~Selected Channel Tracker~~
4. ~~Handle Channel Skip when controller another controller is already on the channel~~
5. Support for up to 4 controllers (currently 2)
6. Dynamic controller ~~and Arduino support~~
7. Nano support
8. ~~Actual Circuit with an actual way to deal with the Ground and VCC~~

#### Maybe/Nice to haves

1. Control all 4 parts from one/two arduino(s)
   - Is the Arduino fast enough? 
     - I think so for two. Unsure about all four
   - Are their serial clocks similar enough to share?
     - Seems like they are
   - I know very little about Direct Port Manipulation and am unsure whether or not I can have multiple outputs



## About the Bit Shifting

The commands sent to the Deck from the Joystick are made up of two bytes. These bytes line up perfectly with the serial clock. 10010000 00000000 would pulse the data line on the first and fourth clock pulse. 

A more efficient sketch for the Arduino would take the two bytes from the Python and shift the bits over on each clock pulse. The bit shifted out would tell the Arduino whether or not to pulse the clock.

Example:

The Arduino receives 00100000 01000001

The Arduino combines the bytes into 0010000001000001. Each clock pulse the Arduino will shift the bits to the left and check the bit shifted out.

1st Clock

0010000001000001 becomes 0100000010000010

If statement runs to check if the bit shifted out is a 1 or 0. If 1 the Data line pulses

2nd Clock

010000001000001 becomes 1000000100000100

If statement runs to check if the bit shifted out is a 1 or 0. The bit shifted out is a 0. The data line stays low

3rd Clock

1000000100000100 becomes 0000001000001000

If statement runs to check if the bit shifted out is a 1 or 0. The bit shifted out is a 1 and the data line drives high until the next clock pulse

.....
