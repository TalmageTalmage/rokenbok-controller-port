# Copyright (c) 20222 Talmage
# Licensed under the MIT License
# See LICENSE.txt for details

import serial
import time
ser=[]
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    h=0
    if "Arduino" in p.description:
        
        ser.append(serial.Serial(p[0], 115200))
        ser[h].write([0x10])
        h = h+1

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


def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
select = []




pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Rokenbok Time')

# Loop until the user clicks the close button.
done = False


# Initialize the joysticks.
pygame.joystick.init()
count = pygame.joystick.get_count()
def selectUp(id):
    select[id]= select[id]+1
    if select[id] > 8:
        select[id]=1
    for j in range(count):
        if select[j] == select[id] and j != id:
                select[id] = select[id] + 1
    if select[id] > 8:
        select[id]=1

textPrint = TextPrint()
    
for i in range(count):
    select.append(0)



# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
        elif event.type == pygame.JOYBUTTONUP:


            if event.button == 6:  # Select
                selectUp(event.instance_id)
                    # if event.joy == 0 :
                    #     select[0]= select[0]+ 1
                    #     if select[0] > 8:
                    #         select[0] = 1
                    #     if select[0] == select[1]:
                    #         select[0] = select[0] + 1
                    # elif event.joy == 1 :
                    #     select[1]= select[1]+ 1
                    #     if select[1] > 8:
                    #         select[1] = 1
                    #     if select[0] == select[1]:
                    #         select[1] = select[1] + 1
        elif event.type ==  pygame.JOYDEVICEREMOVED:
            select.insert(event.instance_id, 0)
            ser.insert(event.instance_id, 0)




                    
    pygame.display.flip()


    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    ROKData= [0x00, 0x00]



 
    textPrint.reset()
    screen.fill(WHITE)


    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
    

    # For each joystick:
    for i in range(joystick_count):
        ROKData[0] = 0x00
        ROKData[1] = 0x00
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
        
        try:
            textPrint.tprint(screen, "Joystick {}".format(jid))
            textPrint.tprint(screen, "Channel {}".format(select[jid]))
        except:
            pass

        try:
            if (convertToInt(ser[jid].read(size=1)) == 0x12): 

                axes = joystick.get_numaxes()

                for i in range(axes):
                    axis = joystick.get_axis(i)

                buttons = joystick.get_numbuttons()

                for i in range(buttons):
                    button = joystick.get_button(i)
                    #A
                    if  i == 0 and button == 1:
                        ROKData[0] = ROKData[0] | 0b00010000
                    #B   
                    if i == 1 and button == 1:
                        ROKData[0] = ROKData[0] | 0b00000001
                    #X
                    if i == 2 and button == 1:
                        ROKData[0] = ROKData[0] | 0b00000010
                    #Y
                    if i == 3 and button == 1:
                        ROKData[0] = ROKData[0] | 0b00001000
                    #Select
                    if i == 6 and button == 1:
                        ROKData[1] = ROKData[1] | 0b00010000

                hats = joystick.get_numhats()

                for i in range(hats):
                    hat = joystick.get_hat(i)

                    #up
                    if hat[1] == 1:
                        ROKData[1] = ROKData[1] | 0b01000000
                    else:
                        ROKData[1] = ROKData[1] & 0b10111111
                    #down
                    if hat[1] == (-1):
                        ROKData[1] = ROKData[1] | 0b00100000
                    else:
                        ROKData[1] = ROKData[1] & 0b11011111
                    #left
                    if hat[0] == (-1):
                        ROKData[1] = ROKData[1] | 0b00000010
                    else:
                        ROKData[1] = ROKData[1] & 0b11111101
                    #right
                    if hat[0] == (1):
                        ROKData[1] = ROKData[1] | 0b10000000
                    else:
                        ROKData[1] = ROKData[1] & 0b01111111
                    try:
                        ser[jid].write([ROKData[0]])
                        ser[jid].write([ROKData[1]])
                    except:
                        
                        pass
        except:
            pass




 
# ---------------TO HERE--------------------
