# General Information 
*note* The Command Deck and controllers use a system that is usually refferred to as Master/Slave or Controller/Target. Because of the deprecation of the former and the potential confusion of the latter, I will be reffering to the Command Deck as the Deck and the controller as a joystick in this seciton. 

The Rokenbok controller port is a female DB9 connector with only 5 pins in use, Ground, VCC, Serial Clock, Data Line, and a Chip Select line. This repo is using the Chip Select Line as a latch. The Data Line works one way, joystick to command deck. I believe the Command Deck can send information to the joystick using the Chip Select Line.

### Communication Protocol

The Command Deck will drive the Chip Select Line Low, signaling to the joystick that it is ready to receive a command. The Deck will drive the serial clock High and then immediately back low. The deck will do this pulse 17 times. Each button is represented by one of the pulses. If that button is pressed the joystick will drive the data line high until the next serial clock pulse. 
