# Copyright (c) 20222 Talmage
# Licensed under the MIT License
# See LICENSE.txt for details

# This script will need to be adjusted depending on how many arduinos/controllers you are using
# You will also need to adjust the COM to match your Arduino's
# 1 arduino is needed for each controller

#Importing Pygame this way prevents that annoying console log at the beginning
import serial
import time
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# Setting arduino connections
# Change this to match your settings
ser = [serial.Serial("COM3", 115200),serial.Serial("COM7", 115200)]
# ser[0] =  serial.Serial("COM3", 115200)
# ser[1] = serial.Serial("COM7", 115200) #-------------comment out if single arduino-----------


time.sleep(2)
# Telling the Arduino(s) to get ready for a command
ser[0].write([0x10])
ser[1].write([0x10])#-------------comment out if single arduino-----------


pygame.init()

screen = pygame.display.set_mode((500, 500))
select = [0, 0]
ROKData =[0x00, 0x00]
ROKData2 =[0x00, 0x00]



# Pygame GUI setup
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

# This just makes it easier to work with bytes in the code
def convertToInt(arrayInput):
    return int(ord(arrayInput[:1]))

# Controller function. Checks states of all buttons then writes to the byte to the Arduino
def joyCommand(ROKData):

    buttons = joystick.get_numbuttons()

    for i in range(buttons):
        button = joystick.get_button(i)
        # A
        if  i == 0 and button == 1:
            ROKData[0] = ROKData[0] | 0b00010000
        # B  
        if i == 1 and button == 1:
            ROKData[0] = ROKData[0] | 0b00000001
        # X
        if i == 2 and button == 1:
            ROKData[0] = ROKData[0] | 0b00000010
        # Y
        if i == 3 and button == 1:
            ROKData[0] = ROKData[0] | 0b00001000
        # Select
        if i == 6 and button == 1:
            ROKData[1] = ROKData[1] | 0b00010000

    hats = joystick.get_numhats()

    for i in range(hats):
        hat = joystick.get_hat(i)

        # UP
        if hat[1] == 1:
            ROKData[1] = ROKData[1] | 0b01000000
            print("yup")
        else:
            ROKData[1] = ROKData[1] & 0b10111111
        # DOWN
        if hat[1] == (-1):
            ROKData[1] = ROKData[1] | 0b00100000
        else:
            ROKData[1] = ROKData[1] & 0b11011111
        # LEFT
        if hat[0] == (-1):
            ROKData[1] = ROKData[1] | 0b00000010
        else:
            ROKData[1] = ROKData[1] & 0b11111101
        # RIGHT
        if hat[0] == (1):
            ROKData[1] = ROKData[1] | 0b10000000
        else:
            ROKData[1] = ROKData[1] & 0b01111111
   
   
    print("%s %s" % (hex(ROKData[0]),hex(ROKData[1])))
    return ROKData
    # ROKData[0] = 0x00
    # ROKData[1] = 0x00

# Handles channel select for the GUI
def selectUp(joy):
    select[joy]= select[joy]+ 1
    if select[joy] > 8:
        select[joy] = 1
    for i in range(select):
        if joy != i and select[joy] == select[i]:
            select[joy] = select[joy] + 1





# Loop until the user clicks the close button
done = False


# Initialize the joysticks
pygame.joystick.init()

textPrint = TextPrint()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.JOYBUTTONDOWN:

# Select GUI
                if event.button == 6:
                    # joy = event.joy
                    # selectUp(joy)
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


    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()


 
    textPrint.reset()
    screen.fill(WHITE)

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
   
    # For each joystick
    for i in range(joystick_count):

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

        if (convertToInt(ser[0].read(size=1)) == 0x12 and jid==0):
            ROKData = joyCommand(ROKData)
            ser[jid].write([ROKData[0]])
            ser[jid].write([ROKData[1]])

            ROKData[0] = 0x00
            ROKData[1] = 0x00
        if (convertToInt(ser[1].read(size=1)) == 0x12 and jid==1): #-------------comment out if single arduino-----------
            ROKData2 = joyCommand(ROKData2)
            ser[jid].write([ROKData2[0]])
            ser[jid].write([ROKData2[1]])
            ROKData2[0] = 0x00
            ROKData2[1] = 0x00


#-------------comment out if single arduino----------- 
