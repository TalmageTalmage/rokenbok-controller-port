# Copyright (c) 20222 Talmage
# Licensed under the MIT License
# See LICENSE.txt for details

import serial
import time
#Adjust for however many arduinos you have hooked up. 1 Arduino = 1 controller port
#There is more data marked below to comment out if you only have 1 arduino
ser =  serial.Serial("COM3", 115200) 
ser1 = serial.Serial("COM7", 115200)

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 40)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 20
        self.y = 20
        self.line_height = 30

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


time.sleep(2)
ser.write([0x10])
ser1.write([0x10])



def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))


pygame.init()

screen = pygame.display.set_mode((500, 700))
select = [0, 0]
click1 = False
ROKData1 = 0x00
ROKData2 = 0x00
ROKData3 = 0x00
ROKData4 = 0x00
ROKData5 = 0x00
ROKData6 = 0x00
ROKData7 = 0x00
ROKData8 = 0x00

# Loop until the user clicks the close button.
done = False


# Initialize the joysticks.
pygame.joystick.init()

textPrint = TextPrint()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
            print("Joystick button released.")
        elif event.type == pygame.JOYBUTTONDOWN:


                if event.button == 6:  # Select
                    if event.joy == 0 :
                        select[0]= select[0]+ 1
                        if select[0] > 8:
                            select[0] = 1
                        if select[0] == select[1]:
                            select[0] = select[0] + 1
                    elif event.joy == 1 :
                        select[1]= select[1]+ 1
                        if select[1] > 8:
                            select[1] = 1
                        if select[0] == select[1]:
                            select[1] = select[1] + 1
                    
    pygame.display.flip()


    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    ROKData1 = 0x00
    ROKData2 = 0x00
    ROKData3 = 0x00
    ROKData4 = 0x00
    ROKData5 = 0x00
    ROKData6 = 0x00
    ROKData7 = 0x00
    ROKData8 = 0x00


 
    textPrint.reset()
    screen.fill(WHITE)


    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
    

    # For each joystick:
    for i in range(joystick_count):

        user = joystick = pygame.joystick.Joystick(i)
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            jid = joystick.get_id()

        name = joystick.get_name()

        try:
            guid = joystick.get_guid()
        except AttributeError:
            pass
        
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.tprint(screen, "Channel {}".format(select[jid]))

        if (convertToInt(ser.read(size=1)) == 0x12 and jid == 0): 

            axes = joystick.get_numaxes()

            for i in range(axes):
                axis = joystick.get_axis(i)

            buttons = joystick.get_numbuttons()

            for i in range(buttons):
                button = joystick.get_button(i)
                #A
                if  i == 0 and button == 1:
                    ROKData1 = ROKData1 | 0b00010000
                #B   
                if i == 1 and button == 1:
                    ROKData1 = ROKData1 | 0b00000001
                #X
                if i == 2 and button == 1:
                    ROKData1 = ROKData1 | 0b00000010
                #Y
                if i == 3 and button == 1:
                    ROKData1 = ROKData1 | 0b00001000
                #Select
                if i == 6 and button == 1:
                    ROKData2 = ROKData2 | 0b00010000


                 


            hats = joystick.get_numhats()


            for i in range(hats):
                hat = joystick.get_hat(i)

                #up
                if hat[1] == 1:
                    ROKData2 = ROKData2 | 0b01000000
                else:
                    ROKData2 = ROKData2 & 0b10111111
                #down
                if hat[1] == (-1):
                    ROKData2 = ROKData2 | 0b00100000
                else:
                    ROKData2 = ROKData2 & 0b11011111
                #left
                if hat[0] == (-1):
                    ROKData2 = ROKData2 | 0b00000010
                else:
                    ROKData2 = ROKData2 & 0b11111101
                #right
                if hat[0] == (1):
                    ROKData2 = ROKData2 | 0b10000000
                else:
                    ROKData2 = ROKData2 & 0b01111111
            
            ser.write([ROKData1])
            ser.write([ROKData2])
            # print("%s %s" % (hex(ROKData1),hex(ROKData2)))

        #----------IF YOU ONLY HAVE 1 ARDUINO START THE COMMENT FROM HERE TO THE END OF THE CODE-------
        if (convertToInt(ser1.read(size=1)) == 0x12 and jid == 1): 

            axes = joystick.get_numaxes()

            for i in range(axes):
                axis = joystick.get_axis(i)

            buttons = joystick.get_numbuttons()
            #NOT WORKING
            for i in range(buttons):
                button = joystick.get_button(i)
            #A
                if  i == 0 and button == 1:
                    ROKData3 = ROKData3 | 0b00010000
                #B   
                if i == 1 and button == 1:
                    ROKData3 = ROKData3 | 0b00000001
                #X
                if i == 2 and button == 1:
                    ROKData3 = ROKData3 | 0b00000010
                #Y
                if i == 3 and button == 1:
                    ROKData3 = ROKData3 | 0b00001000
                #Select
                if i == 6 and button == 1:
                    ROKData4 = ROKData4 | 0b00010000


            hats = joystick.get_numhats()
            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).


            #WORKING WORKING
            for i in range(hats):

                hat = joystick.get_hat(i)
                #up
                if hat[1] == 1:
                    ROKData4 = ROKData4 | 0b01000000
                else:
                    ROKData4 = ROKData4 & 0b10111111
                #down
                if hat[1] == (-1):
                    ROKData4 = ROKData4 | 0b00100000
                else:
                    ROKData4 = ROKData4 & 0b11011111
                #left
                if hat[0] == (-1):
                    ROKData4 = ROKData4 | 0b00000010
                else:
                    ROKData4 = ROKData4 & 0b11111101
                #right
                if hat[0] == (1):
                    ROKData4 = ROKData4 | 0b10000000
                else:
                    ROKData4 = ROKData4 & 0b01111111
            ser1.write([ROKData3])
            ser1.write([ROKData4])
            # print("%s %s" % (hex(ROKData3),hex(ROKData4)))

# ---------------TO HERE--------------------






