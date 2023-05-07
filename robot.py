#!/usr/bin/env python3
"""
    This sample program shows how to control a motor using a joystick. In the
    operator control part of the program, the joystick is read and the value
    is written to the motor.
    Joystick analog values range from -1 to 1 and speed controller inputs also
    range from -1 to 1 making it easy to work together. The program also delays
    a short time in the loop to allow other threads to run. This is generally
    a good idea, especially since the joystick values are only transmitted
    from the Driver Station once every 20ms.
"""

import wpilib
from ctre import WPI_TalonFX



class MyRobot(wpilib.TimedRobot):
    #: update every 0.005 seconds/5 milliseconds (200Hz)
    kUpdatePeriod = 0.005

    def robotInit(self):
        """Robot initialization function"""
        self.motor1 = WPI_TalonFX(1)  # initialize the motor as a Talon on channel 0
        self.motor2 = WPI_TalonFX(3)  # initialize the motor as a Talon on channel 0
        self.motor2.setInverted       # initialize the motor as a Talon on channel 0
        self.stick = wpilib.Joystick(0)  # initialize the joystick on port 0
        self.timer = wpilib.Timer()
        
        print("#"*50)
        self.motor1.setSelectedSensorPosition(100)
        print(self.motor1.getSelectedSensorPosition())
        print("#"*50)

    def autonomousInit(self):
        #self.motor1.setIntegratedSensorPositionToAbsolute()
        #pass
        self.motor1.setSelectedSensorPosition(0)
        self.motor2.setSelectedSensorPosition(0)
        self.SP1 = 10000
        self.SP2 = 10000

    def autonomousPeriodic(self):
        """Runs the motor from a joystick."""
        
        self.encVal1 = self.motor1.getSelectedSensorPosition()
        self.encVal2 = self.motor2.getSelectedSensorPosition()
        if (self.encVal1<self.SP1):
            self.motor1.set(0.1)
        elif (self.encVal1>self.SP1):
            self.motor1.set(-0.1)
        else:
            self.motor1.set(0)

        if (self.encVal2>-self.SP2):
            self.motor2.set(-0.1)
        elif (self.encVal1<-self.SP2):
            self.motor2.set(0.1)
        else:
            self.motor2.set(0)

        if self.encVal1>=(self.SP1*0.95):
            self.SP1 = 0
        elif self.encVal1<=(0):
            self.SP1 = 10000

        if self.encVal2<=-(self.SP2*0.95):
            self.SP2 = 0
        elif self.encVal2>=(0):
            self.SP2 = 10000


            

    def teleopInit(self):
        self.velRightPrev = 0
        self.velLeftPrev = 0

    def teleopPeriodic(self):
        """Runs the motor from a joystick."""
        # Set the motor's output.
        # This takes a number from -1 (100% speed in reverse) to
        # +1 (100% speed going forward)

        self.velRight = (self.stick.getY()+self.stick.getZ())*0.2
        self.velLeft = (self.stick.getY()-self.stick.getZ())*-0.2

        self.velRightDiff = self.velRight-self.velRightPrev
        self.velLeftDiff = self.velLeft-self.velLeftPrev

        if self.velRightDiff>0.1:
            self.velRight = self.velRightPrev+0.1
        elif self.velRightDiff<-0.1:
            self.velRight = self.velRightPrev-0.1
        else:
            self.velRight = self.velRight

        if self.velLeftDiff>0.1:
            self.velLeft = self.velLeftPrev+0.1
        elif self.velLeftDiff<-0.1:
            self.velLeft = self.velLeftPrev-0.1
        else:
            self.velRight = self.velRight
        
        self.motor1.set(self.velRight)
        self.motor2.set(self.velLeft)
        
        self.velRightPrev = self.velRight
        self.velLeftPrev = self.velLeft
        


if __name__ == "__main__":
    wpilib.run(MyRobot)