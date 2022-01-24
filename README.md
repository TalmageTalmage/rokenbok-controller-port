# rokenbok-controller-port
This is a repo for using an Arduino to control a Rokenbok and general documentation on how the controller ports work. This repo includes a way to control by a singular keyboard or multiple controllers. 

# General Information 
*note* The Command Deck and controllers use a system that is usually refferred to as Master/Slave or Controller/Target. Because of the deprecation of the former and the potential confusion of the latter, I will be reffering to the Command Deck as the Deck and the controller as a joystick in this seciton. 

The Rokenbok controller port is a female DB9 connector with only 5 pins in use, Ground, VCC, Serial Clock, Data Line, and a Chip Select line. This repo is using the Chip Select Line as a latch. The Data Line works one way, joystick to command deck. I believe the Command Deck can send information to the joystick using the Chip Select Line.

## Communication Protocol

The Command Deck will drive the Chip Select Line Low, signaling to the joystick that it is ready to receive a command. The Deck will drive the serial clock High and then immediately back low. The deck will do this pulse 17 times. Each button is represented by one of the pulses. If that button is pressed the joystick will drive the data line high until the next serial clock pulse. 



# Installation/Setup
### Hardware

The Arduino will use the following ports:

Serial Clock - Digital 2

Latch - Digital 3

Data - Digital 4

Ground the VCC line from the Command Deck 

### Software
Required Library:

```pip install pyserial```

For controllers support:

```pip install pygame```

For keyboard control:

```pip install pywin32```

1. After getting the libraries, upload the 'Hackenbock.ino' sketch to the Arduino(s). Adjust the sketch as needed depending on the model. 

2. Adjust the Python code to match the COM port of the Arduino(s)

3. Run Controller.py or Keyboard.py

4. Play Rokenbok!

### TO DO:

#### Efficiency:
1. Fix incredibly inefficient controller file 
   - refactor main loop. currently copy pasted for each controller instead of in a function
2. Make Arduino code shift bits. Actually emulate the bytes sent on the original controller
   - Currently just telling it to spike on the right clock if a button is presesed. 
   - This is much less efficient then just reading each bit in a byte. I'll explain [Below](https://github.com/talmageluke/rokenbok-controller-port#about-the-bit-shifting).

#### Functionality: 

1. Add R and L trigger (This one's easy, I've just been lazy and these buttons are not frequently used)
2. Compile into executable
3. Selected Channel Tracker
   - Should be possible through PyGame. Same library I'm currently using for controller support
4. Handle Channel Skip when controller another controller is already on the channel
   - Could just force child mode on - this would allow multiple controllers on the same channel
5. Support for up to 4 controllers (currently 2)
6. Dynamic controller and Arduino support
   - Have to comment out/add code to change number of Arduinos selected.
   - Have to comment out/add code to change number of controllers.
   - Have to reset if controller gets unplugged and you would like to use it again
7. Nano support
8. Actual Circuit with an actual way to deal with the Ground and VCC

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
