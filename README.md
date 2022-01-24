# rokenbok-controller-port
This is a repo for using an Arduino to control a Rokenbok. This repo includes a way to controll by keyboard as well as multiple controllers. 

# Installation
Required
```pip install pyserial```
For controllers
```pip install pygame```
For keyboard control
```pip install pywin32``

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

#### Maybe/Nice to haves

1. Control all 4 parts from one/two arduino(s)
   - Is the Arduino fast enough? 
     - I think so for two. Unsure about all four
   - Are their serial clocks similar enough to share?
     - Seems like they are
   - I know very little about Direct Port Manipulation and am unsure whether or not I can have multiple outputs
