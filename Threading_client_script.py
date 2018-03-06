"""This script is slow AF, there is atleast a lag of 2-3s when the client and host
   are on the same computer! This is just placed as an example of threading, nothing
   more. For the UNCOMPARABLY BETTER performance, use 'client_script.py'
   """
import socket
import sys
import pygame
import threading


# Reads the joystick values and maps them into corresponding pwm values
def readJoystick():
    ga = pygame.joystick.Joystick(0).get_axis
    lk = threading.Lock()
    while True:
        pygame.event.pump()
        (axes[0],axes[1],axes[2],axes[3]) = (ga(0),ga(1),ga(2),ga(3))
        for i in range(numAx):
            with lk:
                global pwm
                pwm[i] = int((axes[i]-MINj)*convRatio + MINp)
            #print pwm
 

# Sends data to the server
def sendData():
    lk = threading.Lock()
    while True:
        with lk:
            global pwm
            message = "%d %d %d %d" % (pwm[0],pwm[1],pwm[2],pwm[3])
        #print 'sending "%s"' % message
        sock.sendall(message)

"""BEGIN INIT"""
if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port on the server given by the caller
    server_address = ("localhost", 10001)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    # Initialise the joystick
    pygame.display.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()

    joyName = pygame.joystick.Joystick(0).get_name()
    print >>sys.stderr, "Name of the joystick:"+joyName
    numAx = pygame.joystick.Joystick(0).get_numaxes()
    print >>sys.stderr,"Number of axis: "+str(numAx)
    axes = [0.0,0.0,0.0,0.0]    #we will get inputs here
    pwm = [1500,1500,1500,1000] #setting some default values which will be sent

    """END INIT"""
    MAXp = 1850
    MINp = 1000
    MAXj = 0.999969482421875
    MINj = -1.0

    convRatio = (MAXp-MINp)/(MAXj-MINj)


            
    #Starting the two concurrent processes

#if __name__ == '__main__':
    t1=threading.Thread(target=readJoystick)
    t2=threading.Thread(target=sendData)
    t1.start()
    t2.start()
"""
while True:
    readJoystick()
    sendData()
"""
