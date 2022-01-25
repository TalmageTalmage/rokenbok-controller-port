
import serial
import time
import win32api

ser =  serial.Serial("COM3", 115200) 

time.sleep(2)
ser.write([0x10])



def main():
	ROKData1 = 0x00
	ROKData2 = 0x00
	while 1:
			
		if (convertToInt(ser.read(size=1)) == 0x12): 
			#select
			if win32api.GetAsyncKeyState(ord('Q')):
				ROKData2 = ROKData2 | 0b00010000
			else:
				ROKData2 = ROKData2 & 0b11101111
			#up
			if win32api.GetAsyncKeyState(ord('W')):
				ROKData2 = ROKData2 | 0b01000000
			else:
				ROKData2 = ROKData2 & 0b10111111
			#down
			if win32api.GetAsyncKeyState(ord('S')):
				ROKData2 = ROKData2 | 0b00100000
			else:
				ROKData2 = ROKData2 & 0b11011111
			#right
			if win32api.GetAsyncKeyState(ord('D')):
				ROKData2 = ROKData2 | 0b10000000
			else:
				ROKData2 = ROKData2 & 0b01111111
			#left
			if win32api.GetAsyncKeyState(ord('A')):
				ROKData2 = ROKData2 | 0b00000010
			else:
				ROKData2 = ROKData2 & 0b11111101
			#A
			if win32api.GetAsyncKeyState(ord('J')):
				ROKData1 = ROKData1 | 0b00010000
			else:
				ROKData1 = ROKData1 & 0b11101111
			#B
			if win32api.GetAsyncKeyState(ord('K')):
				ROKData1 = ROKData1 | 0b00000001
			else:
				ROKData1 = ROKData1 & 0b11111110
			#X
			if win32api.GetAsyncKeyState(ord('U')):
				ROKData1 = ROKData1 | 0b00000010
			else:
				ROKData1 = ROKData1 & 0b11111101
			#Y
			if win32api.GetAsyncKeyState(ord('I')):
				ROKData1 = ROKData1 | 0b00001000
			else:
				ROKData1 = ROKData1 & 0b11110111

				
			ser.write([ROKData1])
			ser.write([ROKData2])
			print("%s %s" % (hex(ROKData1),hex(ROKData2)))

def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
	
if __name__ == "__main__":
	main()