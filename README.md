# rokenbok-controller-port
This is a repo for documenting how the Rokenbok's controller ports function as well as providing the functionality to interact with it using an Arduino.

The purpose of this Readme is only to explain how to set up the Arduino(s), run my scripts and layout a roadmap for future development. You can find my actual documentation on how the original controllers function and communicate with the Command Deck [here.](Documentation/controller-port.md)

You can see a video of this project in action [here.](https://www.youtube.com/watch?v=4-s3MExh7sA)

# Installation/Setup
### Hardware
Pin Connections

*note: The Pins for the DB9 Connector are listed left to right and top to bottom with the long side on top*

| Purpose|  DB9 Pin | Arduino Pin |
| --- | --- | ---|
| VCC | 1 | Any unused non-gnd pin|
| Sel% (Latch) | 2 | Digital 3 |
| Serial Clock | 3 | Digital 2|
| Data | 4 | Digital 4|
| Ground | 5 | GND|

You can find details on the Arduino to Command Deck connections [here](Documentation/Connections.png) and the pinout for the DB9 connector [here.](Documentation/Controller-Pinout.txt)


### Software
Upload the 'Hackenbok.ino' sketch to the Arduino(s). It should be all set up for an Arduino UNO. The correct code to use for an Arduino MEGA in the comments at the top of the file.

Run Controller.exe

Alternatively, if you wish to run and edit the script.

Required Library: ```pip install pyserial```

For controllers support: ```pip install pygame```

For keyboard control: ```pip install pywin32```

1. After getting the libraries, upload the 'Hackenbock.ino' sketch to the Arduino(s). Adjust the sketch as needed depending on the model. 

2. Run Controller.py or Keyboard.py


### TO DO:

#### Efficiency:
1. ~~Fix incredibly inefficient controller file~~
2. Make Arduino code shift bits. Actually emulate the bytes sent on the original controller
   - Currently just telling it to spike on the right clock if a button is presesed. 

#### Functionality: 

1. Add R and L trigger 
2. Compile into executable
3. ~~Selected Channel Tracker~~
4. ~~Handle Channel Skip when controller another controller is already on the channel~~
5. Support for up to 4 controllers 
   - Added but unable to test
6. Dynamic controller ~~and Arduino support~~
7. Nano support
8. ~~Actual Circuit with an actual way to deal with the Ground and VCC~~
9. Build into React App and Express or Django server. Stream video of the Rokenbok and take commands from the website.

#### Maybe/Nice to haves

1. Control all 4 parts from one/two arduino(s)




