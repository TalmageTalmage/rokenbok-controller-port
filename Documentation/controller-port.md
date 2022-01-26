# General Information 

The Rokenbok controller port is a female DB9 connector with only 5 pins in use, Ground, VCC, Serial Clock, Data Line, and Sel%. 

![Pinout](Controller_Pinout.png)

| Purpose|  DB9 Pin | Driven by | Original Wire Color|
| --- | --- | ---| ---|
| VCC | 1 |Command Deck| Black |
| Sel% (Latch) | 2 | Command Deck | Brown |
| Serial Clock | 3 |  Command Deck | Green |
| Data | 4 | Controller | Blue |
| Ground | 5 | - | Yellow |

The VCC supplies 5v power to the controller. The logic level of all the communication lines (Sel%, Data, Serial Clock) is 5v.

The Rokenbok controller has 11 buttons; some older models may have a switch on the back as well. The controller uses two 8 bit parallel-in serial-out [shift registers](https://en.wikipedia.org/wiki/Shift_register) to capture the state of each button before sending the information along the Data line.


### Communication Protocol

Each Clock Cycle has 16 clocks. Each clock represents a button. If that button is pressed then the Controller will drive the Data line HIGH until the beginning of the next clock.

From the start of a Clock Cycle:

1. Command Deck will drive the Sel% LOW, waits for a bit, then drive the Sel% HIGH again.
2. The Command Deck will again drive the Sel% LOW and the immmediately drives it HIGH again. This signals the start of the Serial Clock to the controller
3. The Command Deck will begin pulsing the Clock HIGH and LOW. 
4. The Controller will drive the Data line HIGH or LOW for each Clock depending on the command it is issuing.

Through this process, the controller will send 2 bytes to the Command Deck. The Data line being driven HIGH for a clock reperesents a 1 and driven LOW for a 0.

For example, the Select button is represented by the first clock. If only the Select button is pressed then the controller will only drive the Data line HIGH for the first clock and LOW for the rest. The bytes sent will be 10000000 00000000.

Each of the shift register is responsible for one of the bytes. Pressing a button completes the circuit connecting to shift register. After the SEL% is driven low in step 3, the shift registers will check the button states and create a byte. 0 for each button that is not clicked and 1 for each button that is. 

For example, the A button use the bytes 00000000 01000000. The UP button uses 00000100 00000000. The bytes sent by the controller when both of these buttons are pressed will be 00000100 01000000. The controller will drive the Data line HIGH for the 6th and 10th clock.



## Waveforms/Bytes
*note: The first Serial Clock pulse you see is actually two quick pulses in rapid sucession. The Select button goes inbetween these.*

### NO INPUT
![NoInput](Waveforms/Nothing.png)

Bytes: 00000000 00000000

### SELECT

![SELECT](Waveforms/SELECT.png)

Bytes: 10000000 00000000

Hex: 0x80 0x0

### A
![A](Waveforms/A.png)

Bytes: 00000000 01000000

Hex: 0x0 0x40

### B

![B](Waveforms/B.png)

Bytes: 00000000 00100000

Hex: 0x0 0x20

### X

![X](Waveforms/X.png)

Bytes: 00000000 00010000

Hex: 0x0 0x10

### Y

![Y](Waveforms/Y.png)

Bytes: 00000000 00000100

Hex: 0x0 0x4

### UP

![UP](Waveforms/UP.png)

Bytes: 00000100 00000000
Hex: 0x4 0x0

### DOWN

![DOWN](Waveforms/DOWN.png)

Bytes: 00000010 00000000

Hex: 0x2 0x0

### LEFT

![LEFT](Waveforms/LEFT.png)

Bytes: 00000000 10000000

Hex: 0x0 0x80

### RIGHT

![RIGHT](Waveforms/RIGHT.png)

Bytes: 00000001 00000000

Hex: 0x1 0x0
