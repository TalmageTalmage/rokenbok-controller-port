# General Information 
*note: The system of communication used is traditionally referred to as Master/Slave or Control/Target. The former is now deprecated and the latter is confusing, as the controller is the target and the Command Deck is the controller. For this reason I will just refer to them by their original names, Command Deck and Controller.*


The Rokenbok controller port is a female DB9 connector with only 5 pins in use, Ground, VCC, Serial Clock, Data Line, and a Chip Select line. 
![Pinout](Controller_Pinout.png)

This repo is using the Chip Select Line as a latch. The Data Line works one way, joystick to command deck. I believe the Command Deck can send information to the joystick using the Chip Select Line.

### Communication Protocol

The Command Deck will drive the Chip Select Line Low, signaling to the controller that it is ready to receive a command. The Deck will drive the serial clock High and then immediately back low. The deck will do this pulse 17 times. Each button is represented by one of the pulses. If that button is pressed the joystick will drive the data line high until the next serial clock pulse. 

Essentially, this means the controller is sending over two bytes. Each bit has its place on the Serial Clock.
