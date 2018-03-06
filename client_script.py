import socket
import sys
import pygame
import time

class SignalRelay():

    # Useful global constants
    SLEEPTIME = 0.01            # Sleeping time for sleep funciton
    MAXp = [2000,2000,2000,2000]# Maximum PWM value
    MINp = [1001,1000,1061,1010]# Minimum PWM value
    MAXj = 0.999969482421875    # Maximum value given by Joystick
    MINj = -1.0                 # Minimum value given by Joystick
    convRatio = [(MAXp[i]-MINp[i])/(MAXj-MINj) for i in range(4)] # Corresponding conversion ratio
    host =  '192.168.1.1' # Host to which client will connect
    port =  10001       # Port at host to which client connects
    axes = [0.0,0.0,0.0,0.0]    #we will get inputs here
    pwm = [1500,1500,1500,1000] #setting some default values which will be sent

    
    #NOTE: Channel order in MWC-MSP is Roll Pitch Yaw Throttle Aux 1,2,3,4

    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the server
        server_address = (self.host, self.port)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        self.sock.connect(server_address)

        # Initialise the joystick
        pygame.display.init()
        pygame.joystick.init()
        pygame.joystick.Joystick(0).init()

        self.joyName = pygame.joystick.Joystick(0).get_name()
        print >>sys.stderr, "Name of the joystick:"+self.joyName
        self.numAx = pygame.joystick.Joystick(0).get_numaxes()
        print >>sys.stderr,"Number of axis: "+str(self.numAx)


    # Reads the joystick values and maps them into corresponding pwm values
    def readJoystick(self):
        ga = pygame.joystick.Joystick(0).get_axis
        pygame.event.pump()
        (self.axes[0],self.axes[1],self.axes[2],self.axes[3]) = (ga(0),ga(1),ga(2),ga(3))
        for i in [1,3]:
            self.pwm[i] = int((self.axes[i]-self.MINj)*self.convRatio[i]*-1 + self.MAXp[i]) #taking into consideration inversion of axes
        for i in [0,2]:
            self.pwm[i] = int((self.axes[i]-self.MINj)*self.convRatio[i] + self.MINp[i])

    # Sends data to the server
    def sendData(self):
        message = "%d %d %d %d" % (self.pwm[2],self.pwm[3],self.pwm[0],self.pwm[1])
        self.sock.sendall(message)
        print message

    # Start the main loop
    def start(self):
        while True:
            self.readJoystick()
            self.sendData()
            time.sleep(self.SLEEPTIME)

if __name__ == '__main__':
    s = SignalRelay()
    s.start()







